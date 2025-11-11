"""Tasks module - Data access layer.

Handles all database operations for tasks.
"""

import json
from datetime import datetime
from typing import Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority
from infrastructure.database import BaseRepository, DatabaseConnection


class TaskRepository(BaseRepository):
    """Repository for task data access."""

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize task repository.

        Args:
            db_connection: Database connection instance
        """
        super().__init__(db_connection)

    def create(self, task: Task) -> Task:
        """Create a new task.

        Args:
            task: Task object to create

        Returns:
            Created task with assigned ID
        """
        with self.db.get_connection() as conn:
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

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object or None
        """
        row = self.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return self._row_to_task(row) if row else None

    def get_all(self, user_id: Optional[int] = None) -> list[Task]:
        """Get all tasks, optionally filtered by user_id.

        Args:
            user_id: Optional user ID filter

        Returns:
            List of tasks
        """
        if user_id is not None:
            rows = self.fetch_all("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        else:
            rows = self.fetch_all("SELECT * FROM tasks")

        return [self._row_to_task(row) for row in rows]

    def update(self, task_id: int, task: Task) -> Optional[Task]:
        """Update an existing task.

        Args:
            task_id: Task ID to update
            task: Updated task data

        Returns:
            Updated task or None
        """
        task.updated_at = datetime.utcnow()

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET
                    title = ?, description = ?, status = ?, priority = ?,
                    user_id = ?, project_id = ?, updated_at = ?,
                    due_date = ?, tags = ?
                WHERE id = ?
            """, (
                task.title, task.description,
                task.status.value, task.priority.value,
                task.user_id, task.project_id,
                task.updated_at.isoformat(),
                task.due_date.isoformat() if task.due_date else None,
                json.dumps(task.tags),
                task_id
            ))

            if cursor.rowcount == 0:
                return None

        task.id = task_id
        return task

    def update_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        """Update only the status of a task.

        Args:
            task_id: Task ID
            status: New status

        Returns:
            Updated task or None
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET status = ?, updated_at = ?
                WHERE id = ?
            """, (status.value, datetime.utcnow().isoformat(), task_id))

            if cursor.rowcount == 0:
                return None

        return self.get_by_id(task_id)

    def delete(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False otherwise
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    def _row_to_task(self, row) -> Task:
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
