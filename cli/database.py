import os
import sqlite3


HOME = os.path.expanduser("~")
DB_PATH = os.path.join(HOME,'.url_sentry', 'data.db')

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