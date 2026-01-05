import faiss 
import pickle 
import numpy as np
from src.config.settings import FAISS_INDEX_PATH, DATASTORE_PATH
from src.embeddings.embedder import Embedder

class Retriever:
    def __init__(self):
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))
        print(self.index.d)

        with open(DATASTORE_PATH, "rb") as f:
            datastore = pickle.load(f)
            self.datastore = datastore['chunks']
            
        self.embedder = Embedder()

    def retrieve(self, query: str, k: int = 5, threshold: float = 1.0):
        query_inst = [
            #  "Represent this sentence for searching relevant passages: "+ 
            query
        ]
        q_vec, _ = self.embedder.embed(query_inst)
        
        distances, indices = self.index.search(np.array(q_vec).astype('float32'), k)

        results = []
        for idx, dist in enumerate(indices[0]):
            # if dist <= threshold:
                result_id = indices[0][idx]
                if result_id != -1 and result_id < len(self.datastore):
                    stored_item = self.datastore[result_id]
                    results.append({
                        "text": stored_item["text"], 
                        "metadata": stored_item["metadata"],
                        "score": float(distances[0][idx])
                    })
            
        print("returning")
        return results