import sqlite3


def create_table():
    conn = sqlite3.connect('data.db')
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
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='url_data'")
    if c.fetchone()[0] == 0:
        create_table()
    conn.close()