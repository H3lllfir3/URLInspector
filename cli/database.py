import os
import sqlite3


DB_DIR = os.path.join(os.path.expanduser("~"), '.url_sentry')

os.makedirs(DB_DIR, exist_ok=True)

# Set the absolute path for the database file
DB_FILE = 'data.db'
DB_PATH = os.path.join(DB_DIR, DB_FILE)

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS url_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    title TEXT,
                    status_code INTEGER,
                    body TEXT,
                    js_hash TEXT,
                    content_length INTEGER,
                    added_time TEXT
                )''')
    conn.commit()
    conn.close()

def check_and_create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='url_data'")
    if c.fetchone()[0] == 0:
        create_table()
    conn.close()