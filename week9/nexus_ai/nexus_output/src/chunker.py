from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Tuple

def chunk_documents(docs: List[Tuple[str, str]], chunk_size: int = 300, chunk_overlap: int = 50) -> List[Tuple[str, str]]:
    """Split documents into chunks.
    Returns list of (doc_id, chunk_text).
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc_id, content in docs:
        for chunk in splitter.split_text(content):
            chunks.append((doc_id, chunk))
    return chunks
