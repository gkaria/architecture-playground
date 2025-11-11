"""Shared database used by all services."""
import sqlite3
from contextlib import contextmanager


class SharedDatabase:
    """Shared database connection for all services."""

    def __init__(self, db_path: str = "service_based.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT, description TEXT, status TEXT, priority TEXT,
                    user_id INTEGER, project_id INTEGER,
                    created_at TEXT, updated_at TEXT, due_date TEXT, tags TEXT
                )
            """)
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT, email TEXT, full_name TEXT, created_at TEXT
                )
            """)
            # Projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, description TEXT, owner_id INTEGER, created_at TEXT
                )
            """)
