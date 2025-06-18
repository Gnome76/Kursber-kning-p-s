import os
import sqlite3

DB_PATH = "/mnt/data/database.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            current_price REAL,
            revenue_this_year REAL,
            revenue_next_year REAL,
            shares_outstanding REAL,
            ps1 REAL, ps2 REAL, ps3 REAL, ps4 REAL, ps5 REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_company(name, price, rev_this, rev_next, shares, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO companies (name, current_price, revenue_this_year, revenue_next_year,
                               shares_outstanding, ps1, ps2, ps3, ps4, ps5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, price, rev_this, rev_next, shares, ps1, ps2, ps3, ps4, ps5))
    conn.commit()
    conn.close()

def get_all_companies():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM companies")
    rows = c.fetchall()
    conn.close()
    companies = []
    for row in rows:
        companies.append({
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'rev_this': row[3],
            'rev_next': row[4],
            'shares': row[5],
            'ps': row[6:11]
        })
    return companies

def update_company(id, price, rev_this, rev_next, shares, ps1, ps2, ps3, ps4, ps5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE companies SET
            current_price = ?, revenue_this_year = ?, revenue_next_year = ?,
            shares_outstanding = ?, ps1 = ?, ps2 = ?, ps3 = ?, ps4 = ?, ps5 = ?
        WHERE id = ?
    """, (price, rev_this, rev_next, shares, ps1, ps2, ps3, ps4, ps5, id))
    conn.commit()
    conn.close()

def delete_company(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM companies WHERE id = ?", (id,))
    conn.commit()
    conn.close()
