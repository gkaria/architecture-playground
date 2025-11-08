"""Task domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """Task status enum."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    """Task priority enum."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Task domain model.

    Attributes:
        id: Unique identifier for the task
        title: Task title
        description: Detailed description of the task
        status: Current status (todo/in_progress/done)
        priority: Priority level (low/medium/high)
        user_id: ID of the user assigned to this task
        project_id: ID of the project this task belongs to
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        due_date: Optional due date for the task
        tags: List of tags associated with the task
    """
    title: str
    description: str
    user_id: int
    project_id: int
    id: Optional[int] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value if isinstance(self.status, TaskStatus) else self.status,
            "priority": self.priority.value if isinstance(self.priority, TaskPriority) else self.priority,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
            "due_date": self.due_date.isoformat() if self.due_date and isinstance(self.due_date, datetime) else self.due_date,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task from dictionary representation."""
        # Convert string dates back to datetime objects
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if data.get("due_date") and isinstance(data["due_date"], str):
            data["due_date"] = datetime.fromisoformat(data["due_date"])

        # Convert string enums to enum objects
        if isinstance(data.get("status"), str):
            data["status"] = TaskStatus(data["status"])
        if isinstance(data.get("priority"), str):
            data["priority"] = TaskPriority(data["priority"])

        return cls(**data)
