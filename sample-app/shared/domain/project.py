"""Project domain model."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Project:
    """Project domain model.

    Attributes:
        id: Unique identifier for the project
        name: Project name
        description: Project description
        owner_id: ID of the user who owns this project
        members: List of user IDs who are members of this project
    """
    name: str
    description: str
    owner_id: int
    id: Optional[int] = None
    members: list[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert project to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "members": self.members,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Create project from dictionary representation."""
        return cls(**data)
