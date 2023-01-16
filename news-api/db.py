from sqlite import SQLite
import os
from flask import Flask


def init_db(app: Flask):
    with app.app_context():
        if not os.path.exists('news.db'):
            with SQLite('news.db') as cur:
                cur.execute(
                    """CREATE TABLE articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page TEXT, href TEXT UNIQUE NOT NULL, title TEXT NOT NULL)
                """)
        else:
            print("Database aleady exists.")
