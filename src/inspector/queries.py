from __future__ import annotations

import json
import os
import sqlite3

from .database import check_and_create_table


DB_DIR = os.path.join(os.path.expanduser('~'), '.inspector')

# Set the absolute path for the database file
DB_FILE = 'data.db'
DB_PATH = os.path.join(DB_DIR, DB_FILE)


class UrlData:

    def __init__(self, url, title=None, status_code=None, body=None, js_hash=None, content_length=None):
        self.id = None
        self.url = url
        self.title = title
        self.status_code = status_code
        self.body = body
        self.js_hash = js_hash
        self.content_length = content_length
        self.added_time = None

    def save(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            '''INSERT INTO url_data (url, title, status_code, body, js_hash, content_length, added_time)
                     VALUES (?, ?, ?, ?, ?, ?, datetime('now'))''',
            (
                self.url, self.title, self.status_code,
                self.body, self.js_hash, self.content_length,
            ),
        )
        self.id = c.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get(url):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM url_data WHERE url=?', (url,))
        result = c.fetchone()
        conn.close()
        if result:
            url_data = UrlData(
                url=result[1], title=result[2], status_code=result[3], body=result[4],
                js_hash=result[5], content_length=result[6],
            )
            url_data.id = result[0]
            url_data.added_time = result[-1]
            return url_data
        else:
            return None

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM url_data')
        rows = c.fetchall()
        conn.close()
        url_data_list = []
        for row in rows:
            url_data = UrlData(
                url=row[1], title=row[2], status_code=row[3], body=row[4],
                js_hash=row[5], content_length=row[6],
            )
            url_data.id = row[0]
            url_data.added_time = row[-1]
            url_data_list.append(url_data)
        return json.dumps([ud.__dict__ for ud in url_data_list])

    def update(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            '''UPDATE url_data SET url=?, title=?, status_code=?, body=?, js_hash=?,
                     content_length=? WHERE id=?''',
            (
                self.url, self.title, self.status_code, self.body, self.js_hash,
                self.content_length, self.id,
            ),
        )
        conn.commit()
        conn.close()

    def remove(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM url_data WHERE id=?', (self.id,))
        conn.commit()
        conn.close()


check_and_create_table()
