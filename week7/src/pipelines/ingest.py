import faiss
import pickle
import numpy as np
from pathlib import Path

from src.utils.loaders import load_file
from src.utils.chunker import chunk_text
from src.embeddings.embedder import Embedder
from src.config.settings import FAISS_INDEX_PATH, RAW_DIR, DATASTORE_PATH

def run_ingestion():
    all_chunks_data = []

    for file in RAW_DIR.iterdir():
        if file.is_file():
            print(f"Processing: {file.name}")
            docs = load_file(file)
            for doc in docs:
                meta = {"source": file.name, "page": doc.get("page")+1}
                chunks = chunk_text(doc["text"], meta)
                all_chunks_data.extend(chunks)

    if not all_chunks_data:
        print("No data found")
        return

    texts = [c["text"] for c in all_chunks_data]
    
    embedder = Embedder()
    vectors, dimension = embedder.embed(texts)
    vectors = np.array(vectors).astype('float32')

    index = faiss.IndexHNSWFlat(dimension, 32)
    index.add(vectors)

    datastore = {
        i: all_chunks_data[i] 
        for i in range(len(all_chunks_data))
    }

    faiss.write_index(index, str(FAISS_INDEX_PATH))
    with open(DATASTORE_PATH, "wb") as f:
        pickle.dump(datastore, f)

    print(f"ingested {len(vectors)} chunks.")

if __name__ == "__main__":
    run_ingestion()