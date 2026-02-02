from pathlib import Path
from typing import List, Tuple

def load_documents(source_dir: str) -> List[Tuple[str, str]]:
    docs = []
    base_path = Path(source_dir)
    for file_path in base_path.rglob("*.*"):
        if file_path.suffix.lower() in {".txt", ".md"}:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append((str(file_path), text))
    return docs
