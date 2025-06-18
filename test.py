import os
import sqlite3

DATA_MAPP = "/mnt/data"
DB_SOKVAG = os.path.join(DATA_MAPP, "database.db")

def initiera_databas():
    # OBS: Skapar inte mapp i Streamlit Cloud
    if not os.path.exists(DB_SOKVAG):
        conn = sqlite3.connect(DB_SOKVAG)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS test_tabell (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

def lägg_till_text(text):
    conn = sqlite3.connect(DB_SOKVAG)
    c = conn.cursor()
    c.execute('INSERT INTO test_tabell (text) VALUES (?)', (text,))
    conn.commit()
    conn.close()

def hämta_text():
    conn = sqlite3.connect(DB_SOKVAG)
    c = conn.cursor()
    c.execute('SELECT * FROM test_tabell')
    rader = c.fetchall()
    conn.close()
    return rader

if __name__ == "__main__":
    initiera_databas()
    lägg_till_text("Hej från Streamlit!")
    print(hämta_text())
