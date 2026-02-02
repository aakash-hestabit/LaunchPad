import os
import logging
from typing import List, Tuple
import numpy as np
import faiss
from ..config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = self._load_or_create_index()
        self.id_to_metadata: List[Tuple[str, str]] = []  # (doc_id, chunk_text)

    def _load_or_create_index(self):
        if os.path.exists(settings.faiss_index_path):
            logger.info("Loading FAISS index from %s", settings.faiss_index_path)
            index = faiss.read_index(settings.faiss_index_path)
        else:
            logger.info("Creating new IVFFAISS index with nlist=%d, metric=%s", settings.faiss_index_nlist, settings.faiss_metric)
            metric = faiss.METRIC_L2 if settings.faiss_metric.upper() == "L2" else faiss.METRIC_INNER_PRODUCT
            quantizer = faiss.IndexFlatL2(self.dim) if metric == faiss.METRIC_L2 else faiss.IndexFlatIP(self.dim)
            index = faiss.IndexIVFFlat(quantizer, self.dim, settings.faiss_index_nlist, metric)
            # Index will be trained later when we have vectors
        return index

    def build_index(self, embeddings: np.ndarray, metadata: List[Tuple[str, str]]):
        """Train (if needed) and add embeddings to the index.
        embeddings: (N, dim) array
        metadata: list of (doc_id, chunk_text) same order as embeddings
        """
        if embeddings.shape[1] != self.dim:
            raise ValueError("Embedding dimension mismatch")
        if not self.index.is_trained:
            logger.info("Training FAISS index with %d vectors", embeddings.shape[0])
            self.index.train(embeddings)
        logger.info("Adding %d vectors to FAISS index", embeddings.shape[0])
        self.index.add(embeddings)
        self.id_to_metadata.extend(metadata)
        # persist index
        faiss.write_index(self.index, settings.faiss_index_path)
        logger.info("FAISS index saved to %s", settings.faiss_index_path)

    def search(self, query_embedding: np.ndarray, top_k: int = None) -> List[Tuple[str, str, float]]:
        """Search the index with a query embedding.
        Returns list of (doc_id, chunk_text, score).
        """
        if top_k is None:
            top_k = settings.top_k
        query_vec = np.expand_dims(query_embedding, axis=0).astype(np.float32)
        distances, indices = self.index.search(query_vec, top_k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            doc_id, chunk = self.id_to_metadata[idx]
            # For L2 metric lower distance is better, for inner product higher is better
            score = -dist if settings.faiss_metric.upper() == "L2" else dist
            results.append((doc_id, chunk, score))
        return results
