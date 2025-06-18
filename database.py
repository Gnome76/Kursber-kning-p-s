import os
import sqlite3

DATA_DIR = 'data'
DB_PATH = os.path.join(DATA_DIR, 'database.db')

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            current_price REAL,
            revenue_this_year REAL,
            revenue_next_year REAL,
            shares_outstanding REAL,
            ps1 REAL,
            ps2 REAL,
            ps3 REAL,
            ps4 REAL,
            ps5 REAL
        )
    ''')
    conn.commit()
    conn.close()
