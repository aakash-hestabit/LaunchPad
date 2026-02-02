import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, SecretStr

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):
    openai_api_key: SecretStr = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    openai_embedding_model: str = Field(default="text-embedding-ada-002", env="OPENAI_EMBEDDING_MODEL")
    cohere_api_key: SecretStr | None = Field(default=None, env="COHERE_API_KEY")
    cohere_embedding_model: str = Field(default="embed-english-v3.0", env="COHERE_EMBEDDING_MODEL")
    faiss_index_path: str = Field(default="faiss_index.index", env="FAISS_INDEX_PATH")
    faiss_index_nlist: int = Field(default=100, env="FAISS_INDEX_NLIST")
    faiss_metric: str = Field(default="L2", env="FAISS_METRIC")
    chunk_size: int = Field(default=300, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=50, env="CHUNK_OVERLAP")
    top_k: int = Field(default=10, env="TOP_K")
    re_rank_top_k: int = Field(default=5, env="RE_RANK_TOP_K")
    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
