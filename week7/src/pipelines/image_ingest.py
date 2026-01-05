import uuid
from PIL import Image
from pdf2image import convert_from_path
from src.embeddings.clip_embedder import CLIPEmbedder
from src.utils.ocr import extract_text
from src.utils.caption_image import Captionize 
from src.utils.image_loader import load_images
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class IngestionPipeline:
    def __init__(self):
        self.captioner = Captionize()
        self.embedder = CLIPEmbedder()

    def process_element(self, img, meta=None, idx=-1):
        metadata = dict(meta) if meta is not None else {}
        
        if idx != -1:
            metadata['path'] = f'src/data/images/{idx}.png'
            img.save(metadata['path'])
        
        ocr_text = extract_text(img)
        caption = self.captioner.generate_caption(img)
        vector = self.embedder.embed_image(img)

        return {
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {
                "caption": caption,
                "ocr": ocr_text,
                **metadata
            }
        }
    # def process_file(self, images_to_process, meta):
    # def process_file(self, input_data, meta):
        # images_to_process = load_images(file_path)
        # payloads = []
        
        #
        # if isinstance(input_data, list):
        #     items = input_data
        # else:
        #     items = [(input_data, meta)]

        # for img, meta in items:
        #     
        #     ocr_text = extract_text(img)
        #     caption = self.captioner.generate_caption(img)
        #     vector = self.embedder.embed_image(img)

        #     payloads.append({
        #         "id": str(uuid.uuid4()),
        #         "vector": vector,
        #         "payload": {
        #             "caption": caption,
        #             "ocr": ocr_text,
        #             **meta 
        #         }
        #     })
        # return payloads

# if __name__=='__main__':

#     client = QdrantClient(host='localhost', port=6333)
#     collection_name = 'image_rag'

#     if not client.collection_exists(collection_name):
#         client.create_collection(
#             collection_name=collection_name,
#             vectors_config=VectorParams(size=512, distance=Distance.COSINE)
#         )

#     processed_payloads = IngestionPipeline().process_file('src/data/raw/report.pdf')

#     points = [
#             PointStruct(id=item["id"], vector=item["vector"], payload=item["payload"])
#             for item in processed_payloads
#             ]
#     client.upsert(collection_name=collection_name, points=points)