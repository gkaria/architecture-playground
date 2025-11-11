"""Tasks module - API routing layer.

Defines REST API endpoints for task operations.
"""

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.domain import TaskStatus, TaskPriority
from modules.tasks.service import TaskService
from infrastructure.security import (
    limiter,
    RATE_LIMIT_READ,
    RATE_LIMIT_WRITE,
    RATE_LIMIT_CREATE
)


# Pydantic models for request/response
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


def create_task_router(task_service: TaskService) -> APIRouter:
    """Create and configure the task router.

    Args:
        task_service: Task service instance

    Returns:
        Configured API router
    """
    router = APIRouter(prefix="/tasks", tags=["tasks"])

    @router.post("", response_model=TaskResponse, status_code=201)
    @limiter.limit(RATE_LIMIT_CREATE)
    async def create_task(request: Request, task_data: TaskCreate):
        """Create a new task."""
        try:
            created_task = task_service.create_task(task_data.dict())
            return TaskResponse(**created_task.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

    @router.get("", response_model=list[TaskResponse])
    @limiter.limit(RATE_LIMIT_READ)
    async def get_tasks(request: Request, user_id: Optional[int] = Query(None, gt=0)):
        """Get all tasks, optionally filtered by user_id."""
        try:
            tasks = task_service.get_tasks(user_id)
            return [TaskResponse(**task.to_dict()) for task in tasks]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {str(e)}")

    @router.get("/{task_id}", response_model=TaskResponse)
    @limiter.limit(RATE_LIMIT_READ)
    async def get_task(request: Request, task_id: int):
        """Get a single task by ID."""
        try:
            task = task_service.get_task(task_id)
            if task is None:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            return TaskResponse(**task.to_dict())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve task: {str(e)}")

    @router.put("/{task_id}", response_model=TaskResponse)
    @limiter.limit(RATE_LIMIT_WRITE)
    async def update_task(request: Request, task_id: int, task_data: TaskUpdate):
        """Update an existing task."""
        try:
            updated_task = task_service.update_task(task_id, task_data.dict())
            if updated_task is None:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            return TaskResponse(**updated_task.to_dict())
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

    @router.patch("/{task_id}/status", response_model=TaskResponse)
    @limiter.limit(RATE_LIMIT_WRITE)
    async def update_task_status(request: Request, task_id: int, status_data: TaskStatusUpdate):
        """Update only the status of a task."""
        try:
            updated_task = task_service.update_task_status(task_id, status_data.status)
            if updated_task is None:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            return TaskResponse(**updated_task.to_dict())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update task status: {str(e)}")

    @router.delete("/{task_id}", status_code=204)
    @limiter.limit(RATE_LIMIT_WRITE)
    async def delete_task(request: Request, task_id: int):
        """Delete a task."""
        try:
            deleted = task_service.delete_task(task_id)
            if not deleted:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            return None
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")

    return router
