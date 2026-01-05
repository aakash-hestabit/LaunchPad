from pathlib import Path
# EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
EMBEDDING_MODEL = 'BAAI/bge-base-en-v1.5'
# EMBEDDING_MODEL='BAAI/bge-m3'
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

FAISS_INDEX_PATH = "src/vectorstore/index.faiss"
FAISS_INDEX_PATH2 = "src/vectorstore/index2.faiss"
RAW_DIR = Path("src/data/raw")
DATASTORE_PATH = "src/data/chunks/datastore.pkl"
DATASTORE_PATH2 = "src/data/chunks/datastore2.pkl"