import sqlite3
import os

# create data folder if it does not exist
os.makedirs("data", exist_ok=True)

def create_database():

    conn = sqlite3.connect("data/scraped_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_data(title, price):

    conn = sqlite3.connect("data/scraped_data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products(title, price) VALUES(?, ?)",
        (title, price)
    )

    conn.commit()
    conn.close()