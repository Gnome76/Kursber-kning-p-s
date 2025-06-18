import sqlite3
import os

DATA_DIR = "mnt/data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS bolag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bolag TEXT NOT NULL,
        nuvarande_kurs REAL NOT NULL,
        omsattning_i_ar REAL NOT NULL,
        omsattning_nasta_ar REAL NOT NULL,
        antal_aktier REAL NOT NULL,
        ps1 REAL NOT NULL,
        ps2 REAL NOT NULL,
        ps3 REAL NOT NULL,
        ps4 REAL NOT NULL,
        ps5 REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def insert_company(bolag, nuvarande_kurs, oms_i_ar, oms_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO bolag 
    (bolag, nuvarande_kurs, omsattning_i_ar, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (bolag, nuvarande_kurs, oms_i_ar, oms_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def get_all_companies():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM bolag")
    bolag = c.fetchall()
    conn.close()
    return bolag

def update_company(id, bolag, nuvarande_kurs, oms_i_ar, oms_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    UPDATE bolag SET 
        bolag = ?, 
        nuvarande_kurs = ?, 
        omsattning_i_ar = ?, 
        omsattning_nasta_ar = ?, 
        antal_aktier = ?, 
        ps1 = ?, ps2 = ?, ps3 = ?, ps4 = ?, ps5 = ?
    WHERE id = ?
    """, (bolag, nuvarande_kurs, oms_i_ar, oms_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def delete_company(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM bolag WHERE id = ?", (id,))
    conn.commit()
    conn.close()
