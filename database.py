# database.py

import sqlite3
import os

DB_PATH = "/mnt/data/database.db"

def init_db():
    dir_path = os.path.dirname(DB_PATH)
    if dir_path:  # Undvik fel om dir_path är tom
        os.makedirs(dir_path, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            current_price REAL,
            revenue_this_year REAL,
            revenue_next_year REAL,
            shares_outstanding INTEGER,
            ps1 REAL,
            ps2 REAL,
            ps3 REAL,
            ps4 REAL,
            ps5 REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_company(name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps_values):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO companies 
        (name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, *ps_values))
    conn.commit()
    conn.close()

def get_all_companies():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM companies')
    rows = c.fetchall()
    conn.close()
    return rows

def update_company(company_id, field, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'UPDATE companies SET {field} = ? WHERE id = ?', (value, company_id))
    conn.commit()
    conn.close()

def delete_company(company_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM companies WHERE id = ?', (company_id,))
    conn.commit()
    conn.close()
