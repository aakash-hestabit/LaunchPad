from sentence_transformers import SentenceTransformer
from src.config.settings import EMBEDDING_MODEL

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed(self, chunks):
            
        embeddings = self.model.encode(chunks,normalize_embeddings=True,show_progress_bar=True, batch_size=16)
        dimension = embeddings.shape[1]

        return embeddings,dimension