import sqlite3


class Connector:
    def __init__(self, db_url):
        conn = sqlite3.connect(db_url)
        self.cursor = conn.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]