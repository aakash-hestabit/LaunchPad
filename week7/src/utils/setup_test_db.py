import sqlite3

def create_test_db(db_path="music_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Artists (
        artist_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        genre TEXT,
        country TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sales (
        sale_id INTEGER PRIMARY KEY,
        artist_id INTEGER,
        amount FLOAT,
        sale_date DATE,
        region TEXT,
        FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
    )
    """)

    artists = [
        (1, 'The Data Beats', 'Synthwave', 'USA'),
        (2, 'SQL Queens', 'Pop', 'UK'),
        (3, 'Query Monster', 'Metal', 'Germany') 
    ]
    
    sales = [
        (101, 1, 1500.50, '2023-01-15', 'North America'),
        (102, 1, 2000.00, '2023-06-12', 'Europe'),
        (103, 2, 5000.00, '2023-03-22', 'Global'),
        (104, 3, 1200.00, '2022-12-01', 'Europe'), 
        (105, 2, 3500.00, '2023-11-30', 'North America')
    ]

    cursor.executemany("INSERT OR IGNORE INTO Artists VALUES (?,?,?,?)", artists)
    cursor.executemany("INSERT OR IGNORE INTO Sales VALUES (?,?,?,?,?)", sales)

    conn.commit()
    conn.close()
    print(f"{db_path} created")

if __name__ == "__main__":
    create_test_db()