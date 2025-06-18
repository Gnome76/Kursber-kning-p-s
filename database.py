import sqlite3
import os

DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "database.db")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            revenue_this_year REAL,
            revenue_next_year REAL,
            shares_outstanding REAL,
            ps1 REAL,
            ps2 REAL,
            ps3 REAL,
            ps4 REAL,
            ps5 REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_company(name, price, rev_now, rev_next, shares, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO companies (name, price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, price, rev_now, rev_next, shares, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def get_all_companies():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM companies')
    result = c.fetchall()
    conn.close()
    return result

def update_company(id, price, rev_now, rev_next, shares, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE companies
        SET price=?, revenue_this_year=?, revenue_next_year=?, shares_outstanding=?, ps1=?, ps2=?, ps3=?, ps4=?, ps5=?
        WHERE id=?
    ''', (price, rev_now, rev_next, shares, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def delete_company(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM companies WHERE id=?', (id,))
    conn.commit()
    conn.close()
