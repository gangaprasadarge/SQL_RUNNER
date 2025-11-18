import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "sql_runner.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    age INTEGER,
    country TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    total REAL,
    status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Shippings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    status TEXT,
    customer INTEGER
)
""")

cur.executemany("""
INSERT INTO Customers (first_name, last_name, age, country)
VALUES (?, ?, ?, ?)
""", [
    ("John", "Doe", 30, "USA"),
    ("Robert", "Luna", 22, "USA"),
    ("David", "Robinson", 25, "UK"),
    ("John", "Reinhardt", 22, "UK"),
    ("Betty", "Doe", 28, "UAE"),
])

conn.commit()
conn.close()

print("Database initialized: sql_runner.db created successfully!")
