"""Data Layer - Database access only."""
import sqlite3
import json
from datetime import datetime
from typing import Optional
from contextlib import contextmanager
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority


class TaskRepository:
    """Data access layer for tasks."""

    def __init__(self, db_path: str = "layered.db"):
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
            conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT, description TEXT, status TEXT, priority TEXT,
                    user_id INTEGER, project_id INTEGER,
                    created_at TEXT, updated_at TEXT, due_date TEXT, tags TEXT
                )
            """)

    def create(self, task: Task) -> Task:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, description, status, priority,
                    user_id, project_id, created_at, updated_at, due_date, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task.title, task.description, task.status.value, task.priority.value,
                  task.user_id, task.project_id, task.created_at.isoformat(),
                  task.updated_at.isoformat(),
                  task.due_date.isoformat() if task.due_date else None,
                  json.dumps(task.tags)))
            task.id = cursor.lastrowid
            return task

    def find_all(self, user_id: Optional[int] = None) -> list[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM tasks")
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def find_by_id(self, task_id: int) -> Optional[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return self._row_to_task(row) if row else None

    def update(self, task_id: int, task: Task) -> Optional[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET title=?, description=?, status=?, priority=?,
                    user_id=?, project_id=?, updated_at=?, due_date=?, tags=?
                WHERE id=?
            """, (task.title, task.description, task.status.value, task.priority.value,
                  task.user_id, task.project_id, datetime.utcnow().isoformat(),
                  task.due_date.isoformat() if task.due_date else None,
                  json.dumps(task.tags), task_id))
            return self.find_by_id(task_id) if cursor.rowcount > 0 else None

    def delete(self, task_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    def _row_to_task(self, row) -> Task:
        return Task(
            id=row["id"], title=row["title"], description=row["description"],
            status=TaskStatus(row["status"]), priority=TaskPriority(row["priority"]),
            user_id=row["user_id"], project_id=row["project_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
            tags=json.loads(row["tags"]) if row["tags"] else []
        )
