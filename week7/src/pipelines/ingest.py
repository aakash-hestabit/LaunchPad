import faiss
import pickle
import numpy as np
from pathlib import Path

from src.utils.loaders import load_file
from src.utils.chunker import chunk_text
from src.embeddings.embedder import Embedder
from src.config.settings import FAISS_INDEX_PATH, RAW_DIR, DATASTORE_PATH

import hashlib
from rank_bm25 import BM25Okapi

embedder = Embedder()

def run_ingestion(doc, meta):
    chunks = chunk_text(doc, meta)
    
    texts = [c["text"] for c in chunks]
    vectors, dimension = embedder.embed(texts)
    
    tokenized_corpus = [text.lower().split() for text in texts]
    return {
        "chunks": chunks, 
        "vectors": vectors, 
        "dimension": dimension, 
        "tokens": tokenized_corpus
    }

# def run_ingestion():
#     all_chunks_data = []
#     seen_hashes = set()

#     for file in RAW_DIR.iterdir():
#         if file.is_file():
#             docs = load_file(file)
#             for doc in docs:
#                 meta = {"source": file.name, 
#                         "page": doc.get("page")+1, 
#                         "year": "2024", 
#                         "type": "policy"}
#                 chunks = chunk_text(doc["text"], meta)
                
#                 for chunk in chunks:
#                     chunk_hash = hashlib.sha256(chunk["text"].encode()).hexdigest()
#                     if chunk_hash not in seen_hashes:
#                         all_chunks_data.append(chunk)
#                         seen_hashes.add(chunk_hash)

#     texts = [c["text"] for c in all_chunks_data]
#     print(len(texts))
    
#     embedder = Embedder()
#     vectors, dimension = embedder.embed(texts)
#     index = faiss.IndexHNSWFlat(dimension, 64)
#     index.add(np.array(vectors).astype('float32'))

#     tokenized_corpus = [text.lower().split() for text in texts]
#     bm25_model = BM25Okapi(tokenized_corpus)

#     faiss.write_index(index, str(FAISS_INDEX_PATH))
#     with open(DATASTORE_PATH, "wb") as f:
#         pickle.dump({"chunks": all_chunks_data, "bm25": bm25_model}, f)

# if __name__ == "__main__":
#     run_ingestion()