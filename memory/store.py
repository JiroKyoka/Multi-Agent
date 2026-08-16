import sqlite3
from datetime import datetime
from memory.base import Memory

class SQLiteMemoryStore:

    def __init__(self, db_path="memory.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXESTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, created_at TEXT NOT NULL)
                """
            )

    def add(self, content):
        created_at = datetime.now()

        with self._connect() as conn:
            conn.execute(
                """
                INSER INTO memories (content,created_at) VALUES (?,?)
                """,
                (
                    content, created_at.isoformat()
                )
            )

    def list_all(self):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT content, created_at FROM memories ORDER BY id ASC
                """
            ).fetchall()

        return [Memory(content=row[0], created_at=datetime.fromisoformat(row[1])) for row in rows]