from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, metadata: dict):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=300)

    chunks = splitter.split_text(text)
    return [{"text": chunk, "metadata": metadata} for chunk in chunks]
