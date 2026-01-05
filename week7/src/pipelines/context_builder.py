import pickle
from sklearn.metrics.pairwise import cosine_similarity
from src.config.settings import FAISS_INDEX_PATH, DATASTORE_PATH
from src.embeddings.embedder import Embedder
from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker 
import asyncio

class ContextBuilder:
    def __init__(self, datastore, bm_25):

        self.embedder = Embedder()
        
        self.retriever = HybridRetriever(datastore, bm_25)

        self.datastore = datastore
        self.bm25 = bm_25
            
        self.reranker = Reranker()

    async def build(self, query, filters={ "year": "2024", "type": "policy" }, k=5):
        
        candidate_ids = await self.retriever.search(query)
        candidates = [self.datastore[i] for i in candidate_ids]
        
        #currently disabling the filters to use the pipeline for DAY3 

        # if filters:
        #     candidates = [
        #         c for c in candidates 
        #         if all(c['metadata'].get(key) == val for key, val in filters.items())
        #     ]

        # reranking
        ranked_candidates = await self.reranker.rerank(query, candidates)

        # mmr (diversity selection)
        final_context = self.apply_mmr(query, ranked_candidates, top_k=k)
        return final_context

    def apply_mmr(self, query, candidates, top_k, lambda_param=0.5):
        if not candidates: return []
        
        texts = [c['text'] for c in candidates]
        embeddings, _ = self.embedder.embed(texts)
        query_emb, _ = self.embedder.embed([query])
        
        selected_indices = [0] 
        remaining_indices = list(range(1, len(candidates)))
        
        while len(selected_indices) < top_k and remaining_indices:
            mmr_scores = []
            for i in remaining_indices:
                rel = cosine_similarity([embeddings[i]], query_emb)[0][0]
                redundancy = max([cosine_similarity([embeddings[i]], [embeddings[j]])[0][0] 
                                 for j in selected_indices])
                score = lambda_param * rel - (1 - lambda_param) * redundancy
                mmr_scores.append((i, score))
            
            best_idx = max(mmr_scores, key=lambda x: x[1])[0]
            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)
            
        return [candidates[i] for i in selected_indices]
        