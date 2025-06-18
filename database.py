import sqlite3
import os

DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT,
            nuvarande_kurs REAL,
            omsättning_år REAL,
            omsättning_nästa_år REAL,
            antal_aktier REAL,
            ps1 REAL,
            ps2 REAL,
            ps3 REAL,
            ps4 REAL,
            ps5 REAL
        )
    ''')
    conn.commit()
    conn.close()

def lagg_till_bolag(namn, nuvarande_kurs, omsättning_år, omsättning_nästa_år, antal_aktier,
                    ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bolag (
            namn, nuvarande_kurs, omsättning_år, omsättning_nästa_år,
            antal_aktier, ps1, ps2, ps3, ps4, ps5
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (namn, nuvarande_kurs, omsättning_år, omsättning_nästa_år, antal_aktier,
          ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def hamta_alla_bolag():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bolag')
    bolag = cursor.fetchall()
    conn.close()
    return bolag

def uppdatera_bolag(bolag_id, nuvarande_kurs, omsättning_år, omsättning_nästa_år,
                    antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE bolag SET
            nuvarande_kurs = ?, omsättning_år = ?, omsättning_nästa_år = ?,
            antal_aktier = ?, ps1 = ?, ps2 = ?, ps3 = ?, ps4 = ?, ps5 = ?
        WHERE id = ?
    ''', (nuvarande_kurs, omsättning_år, omsättning_nästa_år,
          antal_aktier, ps1, ps2, ps3, ps4, ps5, bolag_id))
    conn.commit()
    conn.close()

def ta_bort_bolag(bolag_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bolag WHERE id = ?', (bolag_id,))
    conn.commit()
    conn.close()
