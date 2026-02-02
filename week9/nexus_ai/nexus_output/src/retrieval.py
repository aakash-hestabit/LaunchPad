import logging
from typing import List, Tuple

from .embeddings import EmbeddingGenerator
from .vector_store import VectorStore
from ..config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Retriever:
    def __init__(self, vector_store: VectorStore, embedder: EmbeddingGenerator):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int = None) -> List[Tuple[str, str, float]]:
        """Retrieve relevant chunks for a query.
        Returns list of (doc_id, chunk_text, score).
        """
        if top_k is None:
            top_k = settings.top_k
        query_emb = self.embedder.embed([query])[0]
        results = self.vector_store.search(query_emb, top_k=top_k)
        logger.info("Retrieved %d candidates for query", len(results))
        # Optional re‑ranking using cross‑encoder
        if settings.re_rank_top_k and results:
            candidates = [(chunk, score) for _, chunk, score in results]
            reranked = self.embedder.rerank(query, candidates)[: settings.re_rank_top_k]
            # Map back to doc_id using original metadata lookup (simplified)
            # Here we just return chunk and new score; doc_id is unknown after rerank
            reranked_results = []
            for chunk, new_score in reranked:
                # Find original doc_id for this chunk
                for doc_id, c, s in results:
                    if c == chunk:
                        reranked_results.append((doc_id, c, new_score))
                        break
            return reranked_results
        return results
