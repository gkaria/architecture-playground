"""User domain model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User domain model.

    Attributes:
        id: Unique identifier for the user
        username: Unique username
        email: User's email address
        full_name: User's full name
    """
    username: str
    email: str
    full_name: str
    id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert user to dictionary representation."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create user from dictionary representation."""
        return cls(**data)
