import sqlite3
import os

DATA_DIR = "/mnt/data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT UNIQUE NOT NULL,
            nuvarande_kurs REAL NOT NULL,
            omsattning_ars REAL NOT NULL,
            omsattning_nasta_ar REAL NOT NULL,
            antal_aktier INTEGER NOT NULL,
            ps1 REAL NOT NULL,
            ps2 REAL NOT NULL,
            ps3 REAL NOT NULL,
            ps4 REAL NOT NULL,
            ps5 REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hamta_alla_bolag():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM bolag')
    data = c.fetchall()
    conn.close()
    return data

def lagg_till_bolag(namn, nuvarande_kurs, omsattning_ars, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO bolag (namn, nuvarande_kurs, omsattning_ars, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (namn, nuvarande_kurs, omsattning_ars, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def uppdatera_bolag(id, fält, nytt_varde):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = f'UPDATE bolag SET {fält} = ? WHERE id = ?'
    c.execute(query, (nytt_varde, id))
    conn.commit()
    conn.close()

def ta_bort_bolag(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM bolag WHERE id = ?', (id,))
    conn.commit()
    conn.close()
