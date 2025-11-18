import sqlite3
from pathlib import Path

# Absolute DB path (always works regardless of where script is run)
DB = Path(__file__).resolve().parent / "sql_runner.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Enable foreign keys
    cur.execute("PRAGMA foreign_keys = ON;")

    # Create tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        country TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        total REAL,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES Customers(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Shippings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        status TEXT,
        customer INTEGER,
        FOREIGN KEY (order_id) REFERENCES Orders(id)
    );
    """)

    # Insert initial data ONLY if Customers is empty
    cur.execute("SELECT COUNT(*) FROM Customers;")
    if cur.fetchone()[0] == 0:
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
        print("Inserted default Customers data.")

    conn.commit()
    conn.close()

    print(f"Database initialized successfully at: {DB}")


if __name__ == "__main__":
    init_db()