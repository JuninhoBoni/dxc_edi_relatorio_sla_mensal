from conn_sqlite import ConnSqlite
from sqlite3 import Error


def create_table_users():
    try:
        cursor.execute(f"""
        CREATE TABLE {table} (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username        VARCHAR(10) NOT NULL UNIQUE,
                full_name       VARCHAR(100) NOT NULL,
                email           TEXT NOT NULL,
                access_level    INTEGER NOT NULL,
                hashed_password TEXT NOT NULL,
                disabled        BOOLEAN  NOT NULL,
                create_date     DATE NOT NULL
        );
        """)

        print(f"TABLE {table} CREATE".upper())
    except Error as e:
        print(str(e).upper())


def insert_table_users():

    admin = {
        "username": "admin",
        "full_name": "John_Teste",
        "email": "johndoe@example.com",
        "access_level": 0,
        "hashed_password": "$2b$12$fdI3XNTpm8azN8E/YHR3MuM3zjvR9XZq6zcX1y2G9GoHJJ9.vZT.e",
        "disabled": False
    }

    try:
        cursor.execute(f"""
        INSERT INTO {table} (username, full_name, email, access_level, hashed_password, disabled, create_date)
        VALUES (
            '{admin["username"]}',
            '{admin["full_name"]}',
            '{admin["email"]}',
            {admin["access_level"]},
            '{admin["hashed_password"]}',
            {admin["disabled"]},
            date()
        )
        """)

        conn.commit()

        print(f"RECORD INSERTED SUCCESSFULLY IN {table}".upper())

    except Error as e:
        print(str(e).upper())


if __name__ == "__main__":
    conn_sqlite = ConnSqlite()
    conn, cursor = conn_sqlite.conn()
    table = "users"
    create_table_users()
    insert_table_users()
    conn.close()
