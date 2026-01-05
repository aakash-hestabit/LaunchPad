from openai import OpenAI
import yaml 
import os 
from dotenv import load_dotenv
from src.retriever.retriever import Retriever
from src.pipelines.context_builder import ContextBuilder
import asyncio
import time
import pickle
from src.config.settings import DATASTORE_PATH2
load_dotenv()

with open(DATASTORE_PATH2, "rb") as f:
    data_dict = pickle.load(f)
    datastore = data_dict['chunks']
    bm25 = data_dict['bm25']


async def main():
    with open('src/config/model.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key= os.environ['API_KEY']
    )

    query = input("Ask anything: ")
    # results = Retriever().retrieve(query)
    results = await ContextBuilder(datastore,bm25).build(query, k=5)
    print(results)


    SYSTEM_PROMPT = f"""
    Use the following context to answer the question in full detail. 
    If the answer is not in the context, say you don't know.Also, can you guide the user in which file and which page can the user read more about the query.
    If the provided context is not relevant to the question, do not consider it.
    Also tell separartely if you can infer any information from the images attached or data about images

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

if __name__=="__main__":
    asyncio.run(main())