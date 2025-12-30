import faiss
import pickle
import numpy as np
from openai import OpenAI
from src.embeddings.embedder import Embedder
from src.config.settings import FAISS_INDEX_PATH, DATASTORE_PATH
import yaml 



class Retriever:
    def __init__(self):
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))
        
        with open(DATASTORE_PATH, "rb") as f:
            self.datastore = pickle.load(f)
            
        self.embedder = Embedder()

    def retrieve(self, query: str, k: int = 5):
        q_vec, _ = self.embedder.embed([query])
        
        distances, indices = self.index.search(q_vec, k)

        results = []
        for idx, result_id in enumerate(indices[0]):
            if result_id != -1 and result_id in self.datastore:
                stored_item = self.datastore[result_id]
                results.append({
                    "text": stored_item["text"], 
                    "metadata": stored_item["metadata"],
                    "score": float(distances[0][idx])
                })
        
        return results

with open('src/config/model.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=config_data["api_key"] 
)

query = input("Ask anything")
results = Retriever().retrieve(query)
print(results)

SYSTEM_PROMPT = f"""
Use the following context to answer the question in full detail. 
If the answer is not in the context, say you don't know.Also, can you guide the user in which file and which page can the user read more about the query.

Context:
{results}
"""

response = client.chat.completions.create(
    model=config_data["model_name"],
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
)

print(f"\nAI Response:\n{response.choices[0].message.content}")