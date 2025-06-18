import os
import sqlite3

DATA_DIR = 'data'
DB_PATH = os.path.join(DATA_DIR, 'database.db')

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            current_price REAL,
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

def insert_company(name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO companies (name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def get_all_companies():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM companies')
    rows = c.fetchall()
    conn.close()
    return rows

def update_company(id, name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE companies
        SET name=?, current_price=?, revenue_this_year=?, revenue_next_year=?, shares_outstanding=?, ps1=?, ps2=?, ps3=?, ps4=?, ps5=?
        WHERE id=?
    ''', (name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def delete_company(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM companies WHERE id=?', (id,))
    conn.commit()
    conn.close()
