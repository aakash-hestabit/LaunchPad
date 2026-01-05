from qdrant_client import QdrantClient
from src.embeddings.clip_embedder import CLIPEmbedder

class MultimodalRetriever:
    def __init__(self, host="localhost", port=6333, collection_name="image_rag"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.embedder = CLIPEmbedder()


    def search(self, query, mode="text", limit=2):
        if mode == "text":
            query_vector = self.embedder.embed_text(query)
        else:
            query_vector = self.embedder.embed_image(query)

        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True
        ).points