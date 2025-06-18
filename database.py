import sqlite3
import os

DATA_MAPP = "data"
DATABAS_FIL = os.path.join(DATA_MAPP, "databas.db")

def initiera_databas():
    if not os.path.exists(DATA_MAPP):
        os.makedirs(DATA_MAPP, exist_ok=True)
    conn = sqlite3.connect(DATABAS_FIL)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT,
            nuvarande_kurs REAL,
            omsättning_år REAL,
            omsättning_nästa REAL,
            antal_aktier INTEGER,
            ps1 REAL,
            ps2 REAL,
            ps3 REAL,
            ps4 REAL,
            ps5 REAL
        )
    """)
    conn.commit()
    conn.close()

def lägg_till_bolag(namn, nuvarande_kurs, omsättning_år, omsättning_nästa, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DATABAS_FIL)
    c = conn.cursor()
    c.execute("""
        INSERT INTO bolag (
            namn, nuvarande_kurs, omsättning_år, omsättning_nästa,
            antal_aktier, ps1, ps2, ps3, ps4, ps5
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (namn, nuvarande_kurs, omsättning_år, omsättning_nästa, antal_aktier, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def hämta_alla_bolag():
    conn = sqlite3.connect(DATABAS_FIL)
    c = conn.cursor()
    c.execute("SELECT * FROM bolag")
    data = c.fetchall()
    conn.close()
    return data

def uppdatera_bolag(id, nuvarande_kurs, omsättning_år, omsättning_nästa, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DATABAS_FIL)
    c = conn.cursor()
    c.execute("""
        UPDATE bolag
        SET nuvarande_kurs = ?, omsättning_år = ?, omsättning_nästa = ?, 
            antal_aktier = ?, ps1 = ?, ps2 = ?, ps3 = ?, ps4 = ?, ps5 = ?
        WHERE id = ?
    """, (nuvarande_kurs, omsättning_år, omsättning_nästa, antal_aktier, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def ta_bort_bolag(id):
    conn = sqlite3.connect(DATABAS_FIL)
    c = conn.cursor()
    c.execute("DELETE FROM bolag WHERE id = ?", (id,))
    conn.commit()
    conn.close()
