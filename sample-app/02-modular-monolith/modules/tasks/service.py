"""Tasks module - Business logic layer.

Contains business rules, validation, and orchestration logic for tasks.
"""

from datetime import datetime
from typing import Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority
from modules.tasks.repository import TaskRepository
from infrastructure.security import sanitize_string, sanitize_tags


class TaskService:
    """Service layer for task business logic."""

    def __init__(self, repository: TaskRepository):
        """Initialize task service.

        Args:
            repository: Task repository instance
        """
        self.repository = repository
        # Simple in-memory cache
        self._cache: dict[str, tuple[datetime, list[dict]]] = {}
        self._cache_ttl = 60  # seconds

    def create_task(self, task_data: dict) -> Task:
        """Create a new task with business validation.

        Args:
            task_data: Task data dictionary

        Returns:
            Created task

        Raises:
            ValueError: If validation fails
        """
        # Sanitize inputs
        task = Task(
            title=sanitize_string(task_data["title"], max_length=200),
            description=sanitize_string(task_data["description"], max_length=2000),
            status=task_data.get("status", TaskStatus.TODO),
            priority=task_data.get("priority", TaskPriority.MEDIUM),
            user_id=task_data["user_id"],
            project_id=task_data["project_id"],
            due_date=task_data.get("due_date"),
            tags=sanitize_tags(task_data.get("tags", []))
        )

        # Business validation
        if not task.title:
            raise ValueError("Task title cannot be empty")

        created_task = self.repository.create(task)
        self._invalidate_cache()
        return created_task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task or None
        """
        return self.repository.get_by_id(task_id)

    def get_tasks(self, user_id: Optional[int] = None) -> list[Task]:
        """Get tasks with caching.

        Args:
            user_id: Optional user ID filter

        Returns:
            List of tasks
        """
        # Check cache
        cache_key = f"tasks_{user_id}" if user_id else "tasks_all"
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            age = (datetime.utcnow() - cached_time).total_seconds()
            if age < self._cache_ttl:
                return [Task.from_dict(task_dict) for task_dict in cached_data]

        # Cache miss - fetch from repository
        tasks = self.repository.get_all(user_id)
        task_dicts = [task.to_dict() for task in tasks]
        self._cache[cache_key] = (datetime.utcnow(), task_dicts)
        return tasks

    def update_task(self, task_id: int, task_data: dict) -> Optional[Task]:
        """Update a task with business validation.

        Args:
            task_id: Task ID
            task_data: Updated task data

        Returns:
            Updated task or None

        Raises:
            ValueError: If validation fails
        """
        # Check if task exists
        existing_task = self.repository.get_by_id(task_id)
        if existing_task is None:
            return None

        # Create updated task with sanitized inputs
        task = Task(
            id=task_id,
            title=sanitize_string(task_data["title"], max_length=200),
            description=sanitize_string(task_data["description"], max_length=2000),
            status=task_data["status"],
            priority=task_data["priority"],
            user_id=task_data["user_id"],
            project_id=task_data["project_id"],
            created_at=existing_task.created_at,
            due_date=task_data.get("due_date"),
            tags=sanitize_tags(task_data.get("tags", []))
        )

        # Business validation
        if not task.title:
            raise ValueError("Task title cannot be empty")

        updated_task = self.repository.update(task_id, task)
        self._invalidate_cache()
        return updated_task

    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        """Update task status.

        Args:
            task_id: Task ID
            status: New status

        Returns:
            Updated task or None
        """
        updated_task = self.repository.update_status(task_id, status)
        if updated_task:
            self._invalidate_cache()
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False otherwise
        """
        deleted = self.repository.delete(task_id)
        if deleted:
            self._invalidate_cache()
        return deleted

    def _invalidate_cache(self):
        """Invalidate all cached tasks."""
        self._cache.clear()
