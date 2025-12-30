from pathlib import Path

EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

FAISS_INDEX_PATH = "src/vectorstore/index.faiss"
RAW_DIR = Path("src/data/raw")
DATASTORE_PATH = "src/data/chunks/datastore.pkl"