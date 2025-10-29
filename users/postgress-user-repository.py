import psycopg2
from users.user import User, create_user
from users.userrepository import UserRepository

class PostgresUserRepository(UserRepository):
    def __init__(self):
        self._conn = psycopg2.connect(
            "postgresql://postgres:KillMommies123456789+@db.eslpqywpqxjctglkagso.supabase.co:5432/postgres"
        )
        self.cursor = self._conn.cursor()

    def search(self, id: str):
        self.cursor.execute('SELECT * FROM "users" WHERE id = %s', (id,))
        rows = self.cursor.fetchall()
        return rows

    def save(self, user: User):
        new_user = user.to_dto()
        name = new_user.name
        password = new_user.password
        max_level = new_user.level

        query = """
        INSERT INTO users (name, password, level)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        try:
            self.cursor.execute(query, (name, password, max_level))
            user_id = self.cursor.fetchone()[0]
            self._conn.commit()
            return user_id
        except Exception as e:
            self._conn.rollback()
            raise e

    def close(self):
        self.cursor.close()
        self._conn.close()

    def show_all(self):
        self.cursor.execute('SELECT * FROM "users"')
        rows = self.cursor.fetchall()
        return rows


