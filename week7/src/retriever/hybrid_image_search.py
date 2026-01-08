from src.config.settings import DATASTORE_PATH
import pickle 
import asyncio
from src.pipelines.context_builder import ContextBuilder
from src.retriever.image_search import MultimodalRetriever
from openai import OpenAI
from dotenv import load_dotenv
import yaml
import os
from PIL import Image
import base64
from src.pipelines.image_ingest import IngestionPipeline
from io import BytesIO

load_dotenv()

image_ingester = IngestionPipeline()

with open(DATASTORE_PATH, "rb") as f:
    data_dict = pickle.load(f)
    datastore = data_dict['chunks']
    bm25 = data_dict['bm25']

text_search =  ContextBuilder(datastore, bm25)
image_search = MultimodalRetriever()

def detect_query_type(query):
    if isinstance(query, Image.Image):
        return "IMAGE"
    if isinstance(query, str):
        return "TEXT"
    return "UNKNOWN"

# def preprocess_and_encode(image_path, max_dim=1024, quality=80):
#     with Image.open(image_path) as img:
#         if img.mode in ("RGBA", "P"):
#             img = img.convert("RGB")
            
#         img.thumbnail((max_dim, max_dim))
        
#         buffer = BytesIO()
#         img.save(buffer, format="JPEG", quality=quality)
        
#         return base64.b64encode(buffer.getvalue()).decode('utf-8')

async def hybrid_search(query, limit=3):

    text_results = await text_search.build(query, k=5)
    image_results = image_search.search(query)  # i am currently using bnoth image and textual data for text to text also , 
                                                # if we want we can just remove the part where we search the qdrant DB for images related to the textual query
    
    
    # image_context = []
    # for point in image_results:
    #     path = point.payload.get('path')
    #     ocr_data = point.payload.get('ocr')
        
    #     image_context.append(preprocess_and_encode(path))
    #     image_context.append(f"OCR Content: {ocr_data}")
    
    
    print(text_results)
    print()
    print(image_results)
    return {
        "context_text": text_results,
        "context_images": image_results
    }

async def image_hybrid_search(query):
    query_ingest = image_ingester.process_element(query)
    query_text = query_ingest['payload']['caption']+query_ingest['payload']['ocr']
    text_results = await text_search.build(query_text, k=5)
    image_results = image_search.search(query, mode='image')
    # image_context = []
    # for point in image_results:
    #     path = point.payload.get('path')
    #     ocr_data = point.payload.get('ocr')
        
    #     image_context.append(preprocess_and_encode(path))
    #     image_context.append(f"OCR Content: {ocr_data}")
    
    query = query_text
    results = {
        "context_text": text_results,
        "context_images": image_results
    }
    return results


async def main(query ,results, history):
    with open('src/config/model.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key= os.environ['API_KEY']
    )

    # query = input("Ask anything: ")
    # query = Image.open('src/data/images/2.png')
    # if detect_query_type(query) == 'IMAGE':
    #     results = await image_hybrid_search(query)
    # else:
    #     results = await hybrid_search(query)
    
    print(results)


    SYSTEM_PROMPT = f"""
    Use the following context to answer the question in full detail. 
    If the answer is not in the context, say you don't know.Also, can you guide the user in which file and which page can the user read more about the query.
    If the provided context and history is not relevant to the question, do not consider it. Be relevent to the Query

    Context:
    {results}
    """

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=config_data["model_name"],
        messages=messages,
        stream=False
    )

    # print('\n')
    
    # for chunk in stream:
    #     delta = chunk.choices[0].delta.content
    #     if delta:
    #         # for char in delta:
    #         print(delta, end="", flush=True)
    #         #     time.sleep(0.010)

    # print('\n')
    
    return response.choices[0].message.content