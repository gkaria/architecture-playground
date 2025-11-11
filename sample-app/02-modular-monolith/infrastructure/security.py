"""Shared security infrastructure for modular monolith.

Provides rate limiting, input sanitization, and CORS configuration.
Used by all modules to ensure consistent security practices.
"""

import os
import bleach
from slowapi import Limiter
from slowapi.util import get_remote_address


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


def get_cors_origins() -> list[str]:
    """Get CORS origins based on environment.

    Returns:
        List of allowed CORS origins
    """
    cors_origins_env = os.getenv("CORS_ORIGINS", "")

    if cors_origins_env:
        return cors_origins_env.split(",")
    else:
        return [
            "http://localhost:9000",
            "http://127.0.0.1:9000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]


def get_cors_config() -> dict:
    """Get CORS middleware configuration.

    Returns:
        Dictionary with CORS configuration
    """
    return {
        "allow_origins": get_cors_origins(),
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "max_age": 600,
    }


def sanitize_string(text: str, max_length: int = 2000) -> str:
    """Sanitize user input to prevent XSS attacks.

    Args:
        text: Raw user input
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not text:
        return text

    text = text[:max_length]
    sanitized = bleach.clean(text, tags=[], strip=True)
    return sanitized.strip()


def sanitize_tag(tag: str) -> str:
    """Sanitize a single tag.

    Args:
        tag: Raw tag string

    Returns:
        Sanitized tag
    """
    return sanitize_string(tag, max_length=50)


def sanitize_tags(tags: list[str]) -> list[str]:
    """Sanitize a list of tags.

    Args:
        tags: List of raw tag strings

    Returns:
        List of sanitized tags
    """
    if not tags:
        return []

    sanitized = [sanitize_tag(tag) for tag in tags]
    return [tag for tag in sanitized if tag]


# Rate limiting constants
RATE_LIMIT_READ = "100/minute"
RATE_LIMIT_WRITE = "30/minute"
RATE_LIMIT_CREATE = "20/minute"
