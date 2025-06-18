import os, sqlite3
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS bolag (
        id INTEGER PRIMARY KEY,
        namn TEXT, nuvarande_kurs REAL,
        omsattning_i_ar REAL, omsattning_i_nasta_ar REAL,
        antal_aktier INTEGER, ps1 REAL, ps2 REAL, ps3 REAL, ps4 REAL, ps5 REAL
    )''')
    conn.commit(); conn.close()
