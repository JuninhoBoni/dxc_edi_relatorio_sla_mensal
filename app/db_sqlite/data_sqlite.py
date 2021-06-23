from .conn_sqlite import ConnSqlite
from sqlite3 import Error


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    dr = {}
    dr[d['username']] = d
    return dr


class Select:
    def users(self):
        conn_sqlite = ConnSqlite()
        conn, cursor = conn_sqlite.conn()
        cursor.row_factory = dict_factory
        cursor.execute("""
            SELECT * FROM users
        """)
        result = cursor.fetchall()
        conn.close()
        return result


class Insert:
    def users(self):
        conn_sqlite = ConnSqlite()
        conn, cursor = conn_sqlite.conn()
        table = 'users'
        try:
            cursor.execute(f"""
            INSERT INTO {table} (username, full_name, email, access_level, hashed_password, disabled, create_date)
            VALUES (
                '{self.username}',
                '{self.full_name}',
                '{self.email}',
                {self.access_level},
                '{self.hashed_password}',
                {self.disabled},
                date()
            )
            """)

            conn.commit()

            print(f"RECORD INSERTED SUCCESSFULLY IN {table}".upper())
            insert = True

        except Error as e:
            print(str(e).upper())
            insert = False

        conn.close()

        return insert
