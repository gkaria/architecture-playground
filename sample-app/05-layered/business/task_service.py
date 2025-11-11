"""Business Layer - Business logic and validation."""
from typing import Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.domain import Task, TaskStatus


class TaskService:
    """Business logic layer for tasks."""

    def __init__(self, repository):
        self.repository = repository

    def create_task(self, task: Task) -> Task:
        """Create task with business validation."""
        if not task.title or len(task.title) < 1:
            raise ValueError("Title cannot be empty")
        if len(task.description) > 2000:
            raise ValueError("Description too long")
        return self.repository.create(task)

    def get_all_tasks(self, user_id: Optional[int] = None) -> list[Task]:
        """Get all tasks."""
        return self.repository.find_all(user_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self.repository.find_by_id(task_id)

    def update_task(self, task_id: int, task: Task) -> Optional[Task]:
        """Update task with validation."""
        existing = self.repository.find_by_id(task_id)
        if not existing:
            return None
        if not task.title:
            raise ValueError("Title cannot be empty")
        return self.repository.update(task_id, task)

    def delete_task(self, task_id: int) -> bool:
        """Delete task."""
        return self.repository.delete(task_id)
