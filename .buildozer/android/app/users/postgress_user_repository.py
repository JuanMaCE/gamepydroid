import sqlite3
from users.user import User, create_user
from users.userrepository import UserRepository

class PostgresUserRepository (UserRepository):
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                password TEXT,
                level INTEGER
            )
        """)
        self.conn.commit()

    def search(self, name: str):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return self.cursor.fetchall()

    def save(self, user: User):
        new_user = user.to_dto()
        self.cursor.execute(
            "INSERT INTO users (name, password, level) VALUES (?, ?, ?)",
            (new_user.name, new_user.password, new_user.level)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, id: str, level: str):
        self.cursor.execute("UPDATE users SET level = ? WHERE id = ?", (level, id))
        self.conn.commit()

    def search_by_id(self, id: str):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        return self.cursor.fetchall()

    def search_top(self):
        self.cursor.execute("SELECT * FROM users ORDER BY level DESC LIMIT 8")
        return self.cursor.fetchall()

    def show_all(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
