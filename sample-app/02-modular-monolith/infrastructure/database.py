"""Shared database infrastructure for modular monolith.

Provides database connection and base repository functionality.
Each module gets its own repository that extends the base.
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, Any
from contextlib import contextmanager


class DatabaseConnection:
    """Manages SQLite database connections for all modules."""

    def __init__(self, db_path: str = "modular_tasks.db"):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self):
        """Initialize database schema for all modules."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tasks module table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    project_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    due_date TEXT,
                    tags TEXT
                )
            """)

            # Users module table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            # Projects module table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    owner_id INTEGER NOT NULL,
                    members TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            """)


class BaseRepository:
    """Base repository with common database operations.

    Each module's repository should extend this base class.
    """

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize repository with database connection.

        Args:
            db_connection: Database connection instance
        """
        self.db = db_connection

    def execute_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a database query.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Database cursor
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Fetch a single row from database.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Database row or None
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Fetch all rows from database.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            List of database rows
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
