import sqlite3
import os

# Se till att rätt sökväg används
DB_PATH = "/mnt/data/database.db"

def init_db():
    # Skapa mappen om den inte finns
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Skapa databasen och tabellen om de inte redan finns
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
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
    """)
    conn.commit()
    conn.close()

def insert_company(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO companies (
            name, current_price, revenue_this_year, revenue_next_year,
            shares_outstanding, ps1, ps2, ps3, ps4, ps5
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def get_all_companies():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_company(company_id, field, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE companies SET {field} = ? WHERE id = ?", (value, company_id))
    conn.commit()
    conn.close()

def delete_company(company_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.commit()
    conn.close()
