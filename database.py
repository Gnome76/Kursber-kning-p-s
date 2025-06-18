import sqlite3
import os

DATA_KATALOG = "/mnt/data"
DB_SÖKVÄG = os.path.join(DATA_KATALOG, "database.db")

def init_db():
    os.makedirs(DATA_KATALOG, exist_ok=True)
    conn = sqlite3.connect(DB_SÖKVÄG)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT,
            nuvarande_kurs REAL,
            omsättning_i_år REAL,
            omsättning_nästa_år REAL,
            antal_aktier REAL,
            ps_1 REAL,
            ps_2 REAL,
            ps_3 REAL,
            ps_4 REAL,
            ps_5 REAL
        )
    """)
    conn.commit()
    conn.close()

def lägg_till_bolag(namn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_SÖKVÄG)
    c = conn.cursor()
    c.execute("""
        INSERT INTO bolag (namn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps_1, ps_2, ps_3, ps_4, ps_5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (namn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def hämta_bolag():
    conn = sqlite3.connect(DB_SÖKVÄG)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM bolag")
    bolag = c.fetchall()
    conn.close()
    return bolag

def uppdatera_bolag(id, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_SÖKVÄG)
    c = conn.cursor()
    c.execute("""
        UPDATE bolag
        SET nuvarande_kurs = ?, omsättning_i_år = ?, omsättning_nästa_år = ?, antal_aktier = ?,
            ps_1 = ?, ps_2 = ?, ps_3 = ?, ps_4 = ?, ps_5 = ?
        WHERE id = ?
    """, (nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def ta_bort_bolag(id):
    conn = sqlite3.connect(DB_SÖKVÄG)
    c = conn.cursor()
    c.execute("DELETE FROM bolag WHERE id = ?", (id,))
    conn.commit()
    conn.close()
