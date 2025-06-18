import sqlite3
import os

DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bolag TEXT,
            nuvarande_kurs REAL,
            omsättning_år REAL,
            omsättning_nästa_år REAL,
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

def insert_company(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO companies (
            bolag, nuvarande_kurs, omsättning_år, omsättning_nästa_år,
            antal_aktier, ps1, ps2, ps3, ps4, ps5
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def get_all_companies():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM companies')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_company(company_id, field, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'UPDATE companies SET {field} = ? WHERE id = ?', (value, company_id))
    conn.commit()
    conn.close()

def delete_company(company_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM companies WHERE id = ?', (company_id,))
    conn.commit()
    conn.close()
