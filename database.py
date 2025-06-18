import os
import sqlite3

DATA_MAPP = "/mnt/data"
DB_SOKVAG = os.path.join(DATA_MAPP, "database.db")

def initiera_databas():
    # Skapa mappen om den inte finns
    if not os.path.exists(DATA_MAPP):
        os.makedirs(DATA_MAPP)

    # Skapa tabellen om den inte finns
    conn = sqlite3.connect(DB_SOKVAG)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bolag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bolagsnamn TEXT NOT NULL,
            nuvarande_kurs REAL NOT NULL,
            omsättning_i_år REAL NOT NULL,
            omsättning_nästa_år REAL NOT NULL,
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

def lägg_till_bolag(bolagsnamn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_SOKVAG)
    c = conn.cursor()
    c.execute('''
        INSERT INTO bolag (bolagsnamn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (bolagsnamn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def hämta_alla_bolag():
    conn = sqlite3.connect(DB_SOKVAG)
    c = conn.cursor()
    c.execute('SELECT * FROM bolag')
    bolag_lista = c.fetchall()
    conn.close()
    return bolag_lista

def uppdatera_bolag(id, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_SOKVAG)
    c = conn.cursor()
    c.execute('''
        UPDATE bolag SET
        nuvarande_kurs = ?,
        omsättning_i_år = ?,
        omsättning_nästa_år = ?,
        antal_aktier = ?,
        ps1 = ?,
        ps2 = ?,
        ps3 = ?,
        ps4 = ?,
        ps5 = ?
        WHERE id = ?
    ''', (nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def ta_bort_bolag(id):
    conn = sqlite3.connect(DB_SOKVAG)
    c = conn.cursor()
    c.execute('DELETE FROM bolag WHERE id = ?', (id,))
    conn.commit()
    conn.close()
