import sqlite3
import os

DB_PATH = "/mnt/data/database.db"

def init_db():
    # Se till att mappen finns (Streamlit Cloud har /mnt/data som standard, men säkert)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT NOT NULL,
            kurs REAL NOT NULL,
            oms1 REAL NOT NULL,
            oms2 REAL NOT NULL,
            aktier REAL NOT NULL,
            ps1 REAL NOT NULL,
            ps2 REAL NOT NULL,
            ps3 REAL NOT NULL,
            ps4 REAL NOT NULL,
            ps5 REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

def update_bolag(bolag_id, namn, kurs, oms1, oms2, aktier, ps):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE bolag SET
            namn = ?, kurs = ?, oms1 = ?, oms2 = ?, aktier = ?,
            ps1 = ?, ps2 = ?, ps3 = ?, ps4 = ?, ps5 = ?
        WHERE id = ?
    """, (namn, kurs, oms1, oms2, aktier, *ps, bolag_id))
    conn.commit()
    conn.close()
