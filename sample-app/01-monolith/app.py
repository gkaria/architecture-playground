"""Monolithic Task Manager FastAPI application."""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority
from database import Database
from security import (
    limiter,
    get_cors_config,
    sanitize_string,
    sanitize_tags,
    RATE_LIMIT_READ,
    RATE_LIMIT_WRITE,
    RATE_LIMIT_CREATE,
)
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


# Pydantic models for request/response validation
class TaskCreate(BaseModel):
    """Request model for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    user_id: int = Field(..., gt=0)
    project_id: int = Field(..., gt=0)
    due_date: Optional[datetime] = None
    tags: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Request model for updating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    status: TaskStatus
    priority: TaskPriority
    user_id: int = Field(..., gt=0)
    project_id: int = Field(..., gt=0)
    due_date: Optional[datetime] = None
    tags: list[str] = Field(default_factory=list)


class TaskStatusUpdate(BaseModel):
    """Request model for updating task status."""
    status: TaskStatus


class TaskResponse(BaseModel):
    """Response model for a task."""
    id: int
    title: str
    description: str
    status: str
    priority: str
    user_id: int
    project_id: int
    created_at: str
    updated_at: str
    due_date: Optional[str] = None
    tags: list[str]


# Initialize FastAPI app
app = FastAPI(
    title="Task Manager Monolith",
    description="A monolithic implementation of a Task Manager API",
    version="1.0.0"
)

# Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS to allow Task Manager UI to connect
# Using restrictive CORS configuration from security module
cors_config = get_cors_config()
app.add_middleware(CORSMiddleware, **cors_config)

# Initialize database
db = Database()

# Simple in-memory cache for demonstration
cache: dict[str, tuple[datetime, list[dict]]] = {}
CACHE_TTL_SECONDS = 60


def get_cached_tasks(user_id: Optional[int] = None) -> Optional[list[dict]]:
    """Get tasks from cache if available and not expired.

    Args:
        user_id: Optional user ID filter

    Returns:
        Cached tasks or None if cache miss/expired
    """
    cache_key = f"tasks_{user_id}" if user_id else "tasks_all"

    if cache_key in cache:
        cached_time, cached_data = cache[cache_key]
        age = (datetime.utcnow() - cached_time).total_seconds()

        if age < CACHE_TTL_SECONDS:
            return cached_data

    return None


def set_cached_tasks(tasks: list[dict], user_id: Optional[int] = None):
    """Store tasks in cache.

    Args:
        tasks: List of tasks to cache
        user_id: Optional user ID filter
    """
    cache_key = f"tasks_{user_id}" if user_id else "tasks_all"
    cache[cache_key] = (datetime.utcnow(), tasks)


def invalidate_cache():
    """Invalidate all cached tasks."""
    cache.clear()


@app.get("/")
@limiter.limit(RATE_LIMIT_READ)
async def root(request: Request):
    """Root endpoint."""
    return {
        "message": "Task Manager Monolith API",
        "version": "1.0.0",
        "architecture": "monolith"
    }


@app.get("/health")
@limiter.limit(RATE_LIMIT_READ)
async def health_check(request: Request):
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
@limiter.limit(RATE_LIMIT_CREATE)
async def create_task(request: Request, task_data: TaskCreate):
    """Create a new task.

    Args:
        request: FastAPI request object (for rate limiting)
        task_data: Task creation data

    Returns:
        Created task

    Raises:
        HTTPException: If creation fails
    """
    try:
        # Sanitize user inputs to prevent XSS
        task = Task(
            title=sanitize_string(task_data.title, max_length=200),
            description=sanitize_string(task_data.description, max_length=2000),
            status=task_data.status,
            priority=task_data.priority,
            user_id=task_data.user_id,
            project_id=task_data.project_id,
            due_date=task_data.due_date,
            tags=sanitize_tags(task_data.tags)
        )

        created_task = db.create_task(task)
        invalidate_cache()

        return TaskResponse(**created_task.to_dict())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@app.get("/tasks", response_model=list[TaskResponse])
@limiter.limit(RATE_LIMIT_READ)
async def get_tasks(request: Request, user_id: Optional[int] = Query(None, gt=0)):
    """Get all tasks, optionally filtered by user_id.

    Args:
        request: FastAPI request object (for rate limiting)
        user_id: Optional user ID to filter by

    Returns:
        List of tasks

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        # Check cache first
        cached_tasks = get_cached_tasks(user_id)
        if cached_tasks is not None:
            return [TaskResponse(**task) for task in cached_tasks]

        # Cache miss - fetch from database
        tasks = db.get_tasks(user_id=user_id)
        task_dicts = [task.to_dict() for task in tasks]

        # Update cache
        set_cached_tasks(task_dicts, user_id)

        return [TaskResponse(**task_dict) for task_dict in task_dicts]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {str(e)}")


@app.get("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit(RATE_LIMIT_READ)
async def get_task(request: Request, task_id: int):
    """Get a single task by ID.

    Args:
        request: FastAPI request object (for rate limiting)
        task_id: Task ID

    Returns:
        Task details

    Raises:
        HTTPException: If task not found or retrieval fails
    """
    try:
        task = db.get_task(task_id)

        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        return TaskResponse(**task.to_dict())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve task: {str(e)}")


@app.put("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit(RATE_LIMIT_WRITE)
async def update_task(request: Request, task_id: int, task_data: TaskUpdate):
    """Update an existing task.

    Args:
        request: FastAPI request object (for rate limiting)
        task_id: Task ID to update
        task_data: Updated task data

    Returns:
        Updated task

    Raises:
        HTTPException: If task not found or update fails
    """
    try:
        # Check if task exists
        existing_task = db.get_task(task_id)
        if existing_task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        # Create updated task object with sanitized inputs
        task = Task(
            id=task_id,
            title=sanitize_string(task_data.title, max_length=200),
            description=sanitize_string(task_data.description, max_length=2000),
            status=task_data.status,
            priority=task_data.priority,
            user_id=task_data.user_id,
            project_id=task_data.project_id,
            created_at=existing_task.created_at,
            due_date=task_data.due_date,
            tags=sanitize_tags(task_data.tags)
        )

        updated_task = db.update_task(task_id, task)
        invalidate_cache()

        return TaskResponse(**updated_task.to_dict())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
@limiter.limit(RATE_LIMIT_WRITE)
async def update_task_status(request: Request, task_id: int, status_data: TaskStatusUpdate):
    """Update only the status of a task.

    Args:
        request: FastAPI request object (for rate limiting)
        task_id: Task ID to update
        status_data: New status

    Returns:
        Updated task

    Raises:
        HTTPException: If task not found or update fails
    """
    try:
        updated_task = db.update_task_status(task_id, status_data.status)

        if updated_task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        invalidate_cache()

        return TaskResponse(**updated_task.to_dict())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task status: {str(e)}")


@app.delete("/tasks/{task_id}", status_code=204)
@limiter.limit(RATE_LIMIT_WRITE)
async def delete_task(request: Request, task_id: int):
    """Delete a task.

    Args:
        request: FastAPI request object (for rate limiting)
        task_id: Task ID to delete

    Raises:
        HTTPException: If task not found or deletion fails
    """
    try:
        deleted = db.delete_task(task_id)

        if not deleted:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        invalidate_cache()

        return JSONResponse(status_code=204, content=None)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
