"""SQLite database setup and operations for the monolith implementation."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

import sys
sys.path.append(str(Path(__file__).parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority


class Database:
    """SQLite database manager for the monolith."""

    def __init__(self, db_path: str = "tasks.db"):
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
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create tasks table
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

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL
                )
            """)

            # Create projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    owner_id INTEGER NOT NULL,
                    members TEXT,
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            """)

    def create_task(self, task: Task) -> Task:
        """Create a new task.

        Args:
            task: Task object to create

        Returns:
            Created task with assigned ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (
                    title, description, status, priority,
                    user_id, project_id, created_at, updated_at,
                    due_date, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.title,
                task.description,
                task.status.value,
                task.priority.value,
                task.user_id,
                task.project_id,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                task.due_date.isoformat() if task.due_date else None,
                json.dumps(task.tags)
            ))
            task.id = cursor.lastrowid
            return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_task(row)
            return None

    def get_tasks(self, user_id: Optional[int] = None) -> list[Task]:
        """Get all tasks, optionally filtered by user_id.

        Args:
            user_id: Optional user ID to filter by

        Returns:
            List of tasks
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if user_id is not None:
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM tasks")

            rows = cursor.fetchall()
            return [self._row_to_task(row) for row in rows]

    def update_task(self, task_id: int, task: Task) -> Optional[Task]:
        """Update an existing task.

        Args:
            task_id: Task ID to update
            task: Updated task data

        Returns:
            Updated task or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Update timestamp
            task.updated_at = datetime.utcnow()

            cursor.execute("""
                UPDATE tasks SET
                    title = ?,
                    description = ?,
                    status = ?,
                    priority = ?,
                    user_id = ?,
                    project_id = ?,
                    updated_at = ?,
                    due_date = ?,
                    tags = ?
                WHERE id = ?
            """, (
                task.title,
                task.description,
                task.status.value,
                task.priority.value,
                task.user_id,
                task.project_id,
                task.updated_at.isoformat(),
                task.due_date.isoformat() if task.due_date else None,
                json.dumps(task.tags),
                task_id
            ))

            if cursor.rowcount == 0:
                return None

            task.id = task_id
            return task

    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        """Update only the status of a task.

        Args:
            task_id: Task ID to update
            status: New status

        Returns:
            Updated task or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            updated_at = datetime.utcnow().isoformat()

            cursor.execute("""
                UPDATE tasks SET status = ?, updated_at = ?
                WHERE id = ?
            """, (status.value, updated_at, task_id))

            if cursor.rowcount == 0:
                return None

        # Get the updated task after the transaction is committed
        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: Task ID to delete

        Returns:
            True if deleted, False if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Convert database row to Task object.

        Args:
            row: Database row

        Returns:
            Task object
        """
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=TaskStatus(row["status"]),
            priority=TaskPriority(row["priority"]),
            user_id=row["user_id"],
            project_id=row["project_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
            tags=json.loads(row["tags"]) if row["tags"] else []
        )
