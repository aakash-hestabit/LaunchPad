from pathlib import Path
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader

def load_file(path: Path):
    if path.suffix == ".pdf":
        reader = PdfReader(path)
        return [
            {"text": page.extract_text(), "page": i}
            for i, page in enumerate(reader.pages)
        ]

    if path.suffix == ".txt":
        return [{"text": path.read_text(), "page": None}]

    if path.suffix == ".csv":
        df = pd.read_csv(path)
        return [{"text": row.to_json(), "page": i} for i, row in df.iterrows()]

    if path.suffix == ".docx":
        doc = Document(path)
        return [{"text": p.text, "page": i} for i, p in enumerate(doc.paragraphs)]

    raise ValueError("Unsupported file format")
