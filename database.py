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

create_table()