"""Security utilities for the monolith API.

This module provides basic security features:
- Rate limiting to prevent abuse
- Input sanitization to prevent XSS
- CORS configuration helpers
"""

import os
import bleach
from slowapi import Limiter
from slowapi.util import get_remote_address


# Initialize rate limiter
# Using IP address as key for rate limiting
limiter = Limiter(key_func=get_remote_address)


def get_cors_origins() -> list[str]:
    """Get CORS origins based on environment.

    In production (when CORS_ORIGINS env var is set), use the specified origins.
    In development, allow localhost on common ports.

    Returns:
        List of allowed CORS origins
    """
    cors_origins_env = os.getenv("CORS_ORIGINS", "")

    if cors_origins_env:
        # Production: Use environment variable
        return cors_origins_env.split(",")
    else:
        # Development: Allow localhost
        return [
            "http://localhost:9000",  # Task Manager UI (local)
            "http://127.0.0.1:9000",
            "http://localhost:8000",  # Learning Platform (local)
            "http://127.0.0.1:8000",
        ]


def get_cors_config() -> dict:
    """Get CORS middleware configuration.

    Returns more restrictive CORS settings than wildcard (*).

    Returns:
        Dictionary with CORS configuration
    """
    return {
        "allow_origins": get_cors_origins(),
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "max_age": 600,  # Cache preflight requests for 10 minutes
    }


def sanitize_string(text: str, max_length: int = 2000) -> str:
    """Sanitize user input to prevent XSS attacks.

    Args:
        text: Raw user input
        max_length: Maximum allowed length

    Returns:
        Sanitized string safe for storage/display
    """
    if not text:
        return text

    # Truncate to max length
    text = text[:max_length]

    # Remove any HTML tags and potentially dangerous content
    # Allow only safe tags if needed (currently allowing none)
    sanitized = bleach.clean(
        text,
        tags=[],  # No HTML tags allowed
        strip=True  # Strip disallowed tags instead of escaping
    )

    return sanitized.strip()


def sanitize_tag(tag: str) -> str:
    """Sanitize a single tag.

    Args:
        tag: Raw tag string

    Returns:
        Sanitized tag (max 50 chars, no HTML)
    """
    return sanitize_string(tag, max_length=50)


def sanitize_tags(tags: list[str]) -> list[str]:
    """Sanitize a list of tags.

    Args:
        tags: List of raw tag strings

    Returns:
        List of sanitized tags (non-empty only)
    """
    if not tags:
        return []

    sanitized = [sanitize_tag(tag) for tag in tags]

    # Filter out empty tags after sanitization
    return [tag for tag in sanitized if tag]


# Rate limiting decorators for different endpoint types
RATE_LIMIT_READ = "100/minute"   # Read operations (GET)
RATE_LIMIT_WRITE = "30/minute"   # Write operations (POST, PUT, PATCH, DELETE)
RATE_LIMIT_CREATE = "20/minute"  # Create operations (POST)
