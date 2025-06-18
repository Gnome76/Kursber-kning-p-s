import os
import sqlite3

# Mapp för databasfilen
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

def init_db():
    """Skapar data-mapp och databas om de inte finns."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS bolag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        namn TEXT NOT NULL,
        nuvarande_kurs REAL NOT NULL,
        omsattning_i_ar REAL NOT NULL,
        omsattning_nasta_ar REAL NOT NULL,
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

def lagg_till_bolag(namn, nuvarande_kurs, omsattning_i_ar, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    """Lägger till ett nytt bolag i databasen."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO bolag (namn, nuvarande_kurs, omsattning_i_ar, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (namn, nuvarande_kurs, omsattning_i_ar, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def hamta_alla_bolag():
    """Hämtar alla bolag som en lista av tuples."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM bolag")
    bolag = c.fetchall()
    conn.close()
    return bolag

def uppdatera_bolag(id, namn, nuvarande_kurs, omsattning_i_ar, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    """Uppdaterar ett bolags data med angivet id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    UPDATE bolag SET
    namn = ?,
    nuvarande_kurs = ?,
    omsattning_i_ar = ?,
    omsattning_nasta_ar = ?,
    antal_aktier = ?,
    ps1 = ?,
    ps2 = ?,
    ps3 = ?,
    ps4 = ?,
    ps5 = ?
    WHERE id = ?
    """, (namn, nuvarande_kurs, omsattning_i_ar, omsattning_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def ta_bort_bolag(id):
    """Tar bort bolag med angivet id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM bolag WHERE id = ?", (id,))
    conn.commit()
    conn.close()
