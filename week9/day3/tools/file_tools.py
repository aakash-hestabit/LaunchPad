from autogen_core.tools import FunctionTool
import csv
import os
import sqlite3
import pandas as pd
from typing import List, Dict, Any

def inspect_csv(file_path: str) -> dict:
    """
    Inspect CSV structure only.
    Returns column names and total row count.
    Does NOT return data rows.
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    if not file_path.lower().endswith(".csv"):
        return {"error": "Only .csv files are supported."}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        headers = next(reader, [])
        row_count = sum(1 for _ in reader)

    return {
        "file": file_path,
        "rows": row_count,
        "columns": headers,
        "note": "Structure only. No data rows returned."
    }


inspect_csv_tool = FunctionTool(
    inspect_csv,
    name="inspect_csv",
    description="Inspect CSV structure (columns + row count). No data rows returned.",
    strict=True
)

def read_csv(file_path: str) -> dict:
    """
    Read a CSV file with encoding fallback.
    """
    try:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        if not file_path.lower().endswith(".csv"):
            return {"error": "Only .csv files are supported by read_csv."}

        encodings_to_try = ["utf-8", "ISO-8859-1"]
        last_error = None

        max_rows= 10

        for encoding in encodings_to_try:
            try:
                with open(file_path, "r", encoding=encoding, newline="") as f:
                    reader = csv.DictReader(f)
                    headers = reader.fieldnames or []
                    rows = []

                    for i, row in enumerate(reader):
                        if i >= max_rows:
                            break
                        rows.append(row)

                return {
                    "encoding_used": encoding,
                    "headers": headers,
                    "rows": rows,
                    "note": f"Showing first {len(rows)} rows"
                }

            except UnicodeDecodeError as e:
                last_error = e
                continue

        return {
            "error": "Failed to decode CSV with supported encodings",
            "details": str(last_error),
        }

    except Exception as e:
        return f"error: {e}"

read_csv_tool = FunctionTool(
    read_csv,
    name="read_csv",
    description="Reads a csv files and returns headers and rows"
)


def write_csv(file_path: str, rows: List[Dict[str, Any]]) -> str:
    """
    Appends the rows provided to the end of the CSV file
    """
    
    try:
        if not file_path.lower().endswith(".csv"):
            return "Error: Only .csv files are supported by write_csv."

        if not rows:
            return "Error: rows is empty. Provide at least one row."


        headers = list(rows[0].keys())
        with open(file_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        return f"Wrote CSV file: {file_path}"

    except Exception as e:
        return f"Error:{e}"

write_csv_tool = FunctionTool(
    write_csv,
    name="write_csv",
    description="Appends the provided entries to the end of the .csv file."
)

def load_csv_to_sqlite(
    csv_path: str,
    db_path: str,
    table_name: str
) -> str:
    """
    Load a CSV file into SQLite using chunked loading.
    This is the ONLY allowed way to analyze CSV data.
    """
    try:
        if not os.path.exists(csv_path):
            return f"Error: File not found: {csv_path}"

        conn = sqlite3.connect(db_path)

        for chunk in pd.read_csv(csv_path, chunksize=50_000):
            chunk.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

        conn.close()
        return f"CSV '{csv_path}' loaded into SQLite table '{table_name}'."
    
    except Exception as e:
        return f"Error loading CSV: {e}"


load_csv_tool = FunctionTool(
    load_csv_to_sqlite,
    name="load_csv_to_sqlite",
    description="Load a CSV file into SQLite as a table (chunked, safe).",
    strict=True
)


def read_txt(file_path: str) -> str:
    try:
        if not file_path.lower().endswith(".txt"):
            return "Error: Only .txt files supported."

        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"{e}"


def write_txt(file_path: str, content: str) -> str:
    try:
        if not file_path.lower().endswith(".txt"):
            return "Error: Only .txt files supported."

        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Wrote file: {file_path}"
    
    except Exception as e:
        return f"{e}"

def append_txt(file_path: str, content: str) -> str:
    try:
        if not file_path.lower().endswith(".txt"):
            return "Error: Only .txt files are supported by append_txt."

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)

        return f"Appended to text file: {file_path}"
    
    except Exception as e:
        return f"{e}"

read_txt_tool = FunctionTool(
    read_txt,
    name="read_txt",
    description="Read a .txt file and return its content.",
    strict=True
)

write_txt_tool = FunctionTool(
    write_txt,
    name="write_txt",
    description="Write content to a .txt file (overwrite).",
    strict=True
)

append_txt_tool = FunctionTool(
    append_txt,
    name="append_txt",
    description="Append content to a .txt file.",
    strict=True
)

FILE_TOOLS = [
    inspect_csv_tool,
    load_csv_tool,
    read_csv_tool,
    write_csv_tool,
    read_txt_tool,
    write_txt_tool,
    append_txt_tool
]