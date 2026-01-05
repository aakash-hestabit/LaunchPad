import asyncio
import fitz
import io
import pickle
import numpy as np
import faiss
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from rank_bm25 import BM25Okapi

from src.pipelines.ingest import run_ingestion as text_ingestion
from src.pipelines.image_ingest import IngestionPipeline
from src.config.settings import FAISS_INDEX_PATH2, DATASTORE_PATH2

async def process_pdf(file_path):
    doc = fitz.open(file_path)
    all_tasks = []
    image_pipeline = IngestionPipeline()
    
    idx = 0
    for page_index, page in enumerate(doc):
        meta = {"page": page_index + 1, "source": file_path}
        
        text = page.get_text().strip()
        if text:
            all_tasks.append(asyncio.to_thread(text_ingestion, text, meta))

        image_list = page.get_images(full=True)
        if not text and not image_list: # it means that this is a scanned pdf
            pix = page.get_pixmap()
            img_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            all_tasks.append(asyncio.to_thread(image_pipeline.process_element, img_pil, meta, idx))
            idx+=1
        else:
            for img_info in image_list:
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                img_pil = Image.open(io.BytesIO(base_image["image"])).convert("RGB")
                all_tasks.append(asyncio.to_thread(image_pipeline.process_element, img_pil, meta, idx))
                idx+=1

    results = await asyncio.gather(*all_tasks)

    all_text_chunks = []
    all_text_vectors = []
    all_tokenized_corpus = []
    qdrant_points = []
    vector_dim = None

    for res in results:
        if res is None: continue
        
        if "vector" in res:
            qdrant_points.append(
                PointStruct(id=res["id"], vector=res["vector"], payload=res["payload"])
            )
        
        elif "tokens" in res:
            all_text_chunks.extend(res["chunks"])
            all_text_vectors.extend(res["vectors"])
            all_tokenized_corpus.extend(res["tokens"])
            vector_dim = res["dimension"]

    if all_text_vectors:
        
        np_vectors = np.array(all_text_vectors).astype('float32')
        index = faiss.IndexHNSWFlat(vector_dim, 64)
        index.add(np_vectors)
        faiss.write_index(index, str(FAISS_INDEX_PATH2))

        bm25_model = BM25Okapi(all_tokenized_corpus)

        with open(DATASTORE_PATH2, "wb") as f:
            pickle.dump({
                "chunks": all_text_chunks, 
                "bm25": bm25_model
            }, f)

    if qdrant_points:
        client = QdrantClient(host='localhost', port=6333)
        if not client.collection_exists('image_rag'):
            client.create_collection(
                collection_name='image_rag',
                vectors_config=VectorParams(size=len(qdrant_points[0].vector), distance=Distance.COSINE)
            )
        client.upsert(collection_name='image_rag', points=qdrant_points)
    
    print("All data ingested and stored as a batch.")

if __name__ == "__main__":
    asyncio.run(process_pdf('src/data/raw/report.pdf'))