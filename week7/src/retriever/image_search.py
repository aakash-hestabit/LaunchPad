import os 
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.http.models import ScoredPoint
from src.embeddings.clip_embedder import CLIPEmbedder

class MultimodalRetriever:
    def __init__(self, host="localhost", port=6333, collection_name="image_rag"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.embedder = CLIPEmbedder()

    def scored_point_to_dict(self, point: ScoredPoint):
        return {
            "id": point.id,
            "score": point.score,
            "payload": point.payload,
        }


    def search(self, query, mode="text", limit=2):
        if mode == "text":
            query_vector = self.embedder.embed_text(query)
        else:
            query_vector = self.embedder.embed_image(query)

        image_results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True
        ).points

        for r in image_results:

            image_path = r.payload.get('path') 
            
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                img.show()

        results = [self.scored_point_to_dict(p) for p in image_results]
        return results