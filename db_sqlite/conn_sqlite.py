import sqlite3
from typing import Tuple


class ConnSqlite:
    def conn(self) -> Tuple:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        return conn, cursor
