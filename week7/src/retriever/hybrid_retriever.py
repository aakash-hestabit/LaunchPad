import numpy as np
import faiss
import pickle
from src.config.settings import FAISS_INDEX_PATH2, DATASTORE_PATH
from src.embeddings.embedder import Embedder
import asyncio

class HybridRetriever:
    def __init__(self, datastore, bm_25):
        self.index = faiss.read_index(str(FAISS_INDEX_PATH2))
        print(self.index.d)

        self.datastore = datastore
        self.bm25 = bm_25
            
        self.embedder = Embedder()
    async def dense_search(self, query, top_k):
        q_vec, _ = self.embedder.embed([query])
        distances, indices = self.index.search(q_vec.astype("float32"), top_k)
        return indices[0]

    async def sparse_search(self, query, top_k):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        return np.argsort(scores)[::-1][:top_k]
    
    async def search(self, query, top_k=20):
        dense_task = self.dense_search(query, top_k)
        sparse_task = self.sparse_search(query, top_k)

        dense_ids, sparse_ids = await asyncio.gather(
            dense_task, sparse_task
        )
        print(f"Dense : {dense_ids}")
        print(f"Sparse : {sparse_ids}")

        return self._rrf(dense_ids, sparse_ids)
        

    def _rrf(self, dense_ids, sparse_ids, k=60):
        scores = {}
        for rank, idx in enumerate(dense_ids):
            if idx == -1: continue
            scores[idx] = scores.get(idx, 0) + 1 / (k + rank)
        for rank, idx in enumerate(sparse_ids):
            scores[idx] = scores.get(idx, 0) + 1 / (k + rank)
        return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)