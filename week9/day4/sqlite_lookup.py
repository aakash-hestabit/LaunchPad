import sqlite3

def view_all_memories(db_name="memory/long_term.db"):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM memories")
        rows = cursor.fetchall()

        if not rows:
            print("The database is currently empty.")
            return

        print(f"{'ID':<20} | {'Timestamp':<20} | {'Content'}")
        print("-" * 70)
        
        for row in rows:
            mem_id, content, category, importance, timestamp = row
            print(f"{mem_id:<20} | {timestamp:<20} | {content} | {category} | {importance}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    view_all_memories()