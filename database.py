import sqlite3
import os

DB_PATH = "data/database.db"

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT,
            kurs REAL,
            oms1 REAL,
            oms2 REAL,
            aktier REAL,
            ps1 REAL,
            ps2 REAL,
            ps3 REAL,
            ps4 REAL,
            ps5 REAL
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
        UPDATE bolag
        SET namn=?, kurs=?, oms1=?, oms2=?, aktier=?, ps1=?, ps2=?, ps3=?, ps4=?, ps5=?
        WHERE id=?
    """, (namn, kurs, oms1, oms2, aktier, *ps, bolag_id))
    conn.commit()
    conn.close()
