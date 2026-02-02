import sqlite3
import traceback
from autogen_core.tools import FunctionTool
db_path = "sales.db"

def extract_schema(db_path: str) -> dict:
    """
    Extract full SQLite schema: tables + columns.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema = {}

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    tables = cursor.fetchall()

    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        cols = cursor.fetchall()

        schema[table] = [
            {
                "column": c[1],
                "type": c[2],
                "nullable": not bool(c[3]),
                "primary_key": bool(c[5])
            }
            for c in cols
        ]

    conn.close()
    return schema

def _is_read_only_sql(sql: str) -> bool:
    sql = sql.strip().lower()
    return sql.startswith("select") or sql.startswith("with")

def validate_sql(sql: str):
    tokens = sql.lower().replace(",", " ").split()
    for table, cols in valid_columns.items():
        for token in tokens:
            if token in ["quantity", "sale_date", "price"]:
                if token not in cols:
                    return False, f"Column '{token}' not in schema"
    return True, None

schema = extract_schema(db_path)
valid_columns = {
    table: {col["column"].lower() for col in cols}
    for table, cols in schema.items()
}

def schema_aware_query(
    db_path: str,
    sql: str,
    max_rows: int
) -> dict:
    """
    Execute read-only SQL
    Return schema + query results
    """

    try:
        if not _is_read_only_sql(sql):
            return {
                "error": "Only SELECT / WITH queries are allowed."
            }

        ok, err = validate_sql(sql)
        if not ok:
            return {"error": err}

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql)

        max_rows = min(max_rows, 10)

        rows = cursor.fetchmany(max_rows)
        columns = [d[0] for d in cursor.description] if cursor.description else []
        conn.close()

        return {
            "query": sql,
            "columns": columns,
            "rows": rows
        }

    except Exception:
        return {
            "error": traceback.format_exc()
        }


schema_query_tool = FunctionTool(
    schema_aware_query,
    name="schema_aware_query",
    description="""
Run a read-only SQL query on SQLite.
This tool ALWAYS extracts the database schema before executing the query.
Only SELECT / WITH queries are allowed.
""",
    strict=True
)

extract_schema_tool = FunctionTool(
    extract_schema,
    name="extract_schema_tool",
    description="""
Extracts the SCHEMA of the given DATABASE
""",
    strict=True
)