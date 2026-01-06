import sqlite3

class SchemaLoader:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_schema_string(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        schema_parts = []
        for table_name in [t[0] for t in tables]:

            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            col_desc = [f"{col[1]} ({col[2]})" for col in columns]
            
            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            fks = cursor.fetchall()
            fk_desc = [f"FOREIGN KEY ({fk[3]}) REFERENCES {fk[2]}({fk[4]})" for fk in fks]
            
            table_info = f"Table {table_name}: {', '.join(col_desc)}"
            if fk_desc:
                table_info += f" | Relationships: {', '.join(fk_desc)}"
            schema_parts.append(table_info)
        
        conn.close()
        return "\n".join(schema_parts)