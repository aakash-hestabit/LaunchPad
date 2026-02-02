import os
import logging
from typing import List, Tuple

import numpy as np
from openai import OpenAI
import cohere
from sentence_transformers import CrossEncoder

from ..config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmbeddingGenerator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
        self.cohere_client = None
        if settings.cohere_api_key:
            self.cohere_client = cohere.Client(api_key=settings.cohere_api_key.get_secret_value())
        # cross-encoder for re-ranking (optional)
        self.rerank_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def _embed_openai(self, texts: List[str]) -> List[List[float]]:
        logger.info("Generating embeddings via OpenAI for %d texts", len(texts))
        # OpenAI embeddings API batch limit is 2048 tokens per request; we send batch
        response = self.openai_client.embeddings.create(model=settings.openai_embedding_model, input=texts)
        return [list(emb.embedding) for emb in response.data]

    def _embed_cohere(self, texts: List[str]) -> List[List[float]]:
        if not self.cohere_client:
            raise RuntimeError("Cohere API key not configured")
        logger.info("Generating embeddings via Cohere for %d texts", len(texts))
        response = self.cohere_client.embed(model=settings.cohere_embedding_model, texts=texts)
        return response.embeddings

    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts.
        Tries OpenAI first, falls back to Cohere if configured.
        Returns a NumPy array of shape (len(texts), dim).
        """
        try:
            embeddings = self._embed_openai(texts)
        except Exception as e:
            logger.warning("OpenAI embedding failed: %s", e)
            if self.cohere_client:
                embeddings = self._embed_cohere(texts)
            else:
                raise
        return np.array(embeddings, dtype=np.float32)

    def rerank(self, query: str, candidates: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """Re-rank candidate chunks using a cross‑encoder.
        candidates: list of (chunk_text, score) tuples from initial retrieval.
        Returns a new list sorted by cross‑encoder score descending.
        """
        if not candidates:
            return []
        texts = [c[0] for c in candidates]
        scores = self.rerank_model.predict([[query, txt] for txt in texts])
        reranked = sorted(zip(texts, scores), key=lambda x: x[1], reverse=True)
        return reranked
