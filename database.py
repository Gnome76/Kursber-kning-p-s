import os
import sqlite3

# Sökväg till datamappen och databasen
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

# Initiera databasen och skapa tabellen om den inte finns
def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namn TEXT NOT NULL,
            nuvarande_kurs REAL,
            omsattning_i_ar REAL,
            omsattning_i_nasta_ar REAL,
            antal_aktier INTEGER,
            ps1 REAL,
            ps2 REAL,
            ps3 REAL,
            ps4 REAL,
            ps5 REAL
        )
    ''')
    conn.commit()
    conn.close()

# Lägg till ett nytt bolag
def insert_bolag(namn, nuv_kurs, oms_i_ar, oms_n_ar, antal, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO bolag (namn, nuvarande_kurs, omsattning_i_ar, omsattning_i_nasta_ar,
                           antal_aktier, ps1, ps2, ps3, ps4, ps5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (namn, nuv_kurs, oms_i_ar, oms_n_ar, antal, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

# Hämta alla bolag
def get_alla_bolag():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute('SELECT * FROM bolag')
    bolag = cursor.fetchall()
    conn.close()
    return bolag

# Uppdatera befintligt bolag
def uppdatera_bolag(id, namn, nuv_kurs, oms_i_ar, oms_n_ar, antal, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        UPDATE bolag
        SET namn=?, nuvarande_kurs=?, omsattning_i_ar=?, omsattning_i_nasta_ar=?,
            antal_aktier=?, ps1=?, ps2=?, ps3=?, ps4=?, ps5=?
        WHERE id=?
    ''', (namn, nuv_kurs, oms_i_ar, oms_n_ar, antal, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

# Ta bort ett bolag
def ta_bort_bolag(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('DELETE FROM bolag WHERE id=?', (id,))
    conn.commit()
    conn.close()
