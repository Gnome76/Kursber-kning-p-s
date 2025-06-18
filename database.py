import sqlite3
import os

DATA_MAPP = "/mnt/data"
DB_PATH = os.path.join(DATA_MAPP, "database.db")

def init_db():
    # Skapa mapp om den inte finns
    os.makedirs(DATA_MAPP, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bolag TEXT NOT NULL,
            nuvarande_kurs REAL NOT NULL,
            omsattning_i_år REAL NOT NULL,
            omsattning_nasta_år REAL NOT NULL,
            antal_aktier INTEGER NOT NULL,
            ps1 REAL NOT NULL,
            ps2 REAL NOT NULL,
            ps3 REAL NOT NULL,
            ps4 REAL NOT NULL,
            ps5 REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_bolag(bolag, nuvarande_kurs, omsattning_i_år, omsattning_nasta_år,
                 antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bolag (
            bolag, nuvarande_kurs, omsattning_i_år, omsattning_nasta_år,
            antal_aktier, ps1, ps2, ps3, ps4, ps5
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (bolag, nuvarande_kurs, omsattning_i_år, omsattning_nasta_år,
          antal_aktier, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def hamta_alla_bolag():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM bolag")
    rader = cur.fetchall()
    conn.close()
    # Konvertera till lista av dicts
    return [dict(rad) for rad in rader]

def uppdatera_bolag(id, nuvarande_kurs, omsattning_i_år, omsattning_nasta_år,
                    antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE bolag SET
            nuvarande_kurs = ?,
            omsattning_i_år = ?,
            omsattning_nasta_år = ?,
            antal_aktier = ?,
            ps1 = ?,
            ps2 = ?,
            ps3 = ?,
            ps4 = ?,
            ps5 = ?
        WHERE id = ?
    """, (nuvarande_kurs, omsattning_i_år, omsattning_nasta_år,
          antal_aktier, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def ta_bort_bolag(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM bolag WHERE id = ?", (id,))
    conn.commit()
    conn.close()
