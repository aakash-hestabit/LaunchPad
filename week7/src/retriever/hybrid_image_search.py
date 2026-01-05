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
from src.pipelines.image_ingest import IngestionPipeline

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

async def hybrid_search(query, limit=3):

    text_results = await text_search.build(query, k=5)
    image_results = image_search.search(query)
    
    
    print(text_results)
    print()
    print(image_results)
    return {
        "context_text": text_results,
        "context_images": image_results
    }


async def main():
    with open('src/config/model.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key= os.environ['API_KEY']
    )

    # query = input("Ask anything: ")
    query = Image.open('src/data/images/0.png')
    if detect_query_type(query) == 'IMAGE':
        query_ingest = image_ingester.process_element(query)
        query_text = query_ingest['payload']['caption']+query_ingest['payload']['ocr']
        text_results = await text_search.build(query_text, k=5)
        image_results = image_search.search(query, mode='image')
        query = query_text
        results = {
            "context_text": text_results,
            "context_images": image_results
        }
    else:
        results = await hybrid_search(query)
    
    print(results)


    SYSTEM_PROMPT = f"""
    Use the following context to answer the question in full detail. 
    If the answer is not in the context, say you don't know.Also, can you guide the user in which file and which page can the user read more about the query.
    If the provided context is not relevant to the question, do not consider it.

    Context:
    {results}
    """

    stream = client.chat.completions.create(
        model=config_data["model_name"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        stream=True
    )

    print('\n')
    
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            # for char in delta:
            print(delta, end="", flush=True)
            #     time.sleep(0.010)

    print('\n')
    for r in results['context_images']:

        image_path = r.payload.get('path') 
        
        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            img.show()
        

if __name__=="__main__":
    asyncio.run(main())