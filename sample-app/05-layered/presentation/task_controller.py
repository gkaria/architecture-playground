"""Presentation Layer - HTTP handling."""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    user_id: int = Field(..., gt=0)
    project_id: int = Field(..., gt=0)
    due_date: Optional[datetime] = None
    tags: list[str] = []

class TaskResponse(BaseModel):
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


class TaskController:
    """Presentation layer controller."""

    def __init__(self, service):
        self.service = service
        self.router = APIRouter(prefix="/tasks", tags=["tasks"])
        self._register_routes()

    def _register_routes(self):
        @self.router.post("", response_model=TaskResponse, status_code=201)
        async def create(task_data: TaskCreate):
            task = Task(**task_data.dict())
            created = self.service.create_task(task)
            return TaskResponse(**created.to_dict())

        @self.router.get("", response_model=list[TaskResponse])
        async def get_all(user_id: Optional[int] = Query(None)):
            tasks = self.service.get_all_tasks(user_id)
            return [TaskResponse(**t.to_dict()) for t in tasks]

        @self.router.get("/{task_id}", response_model=TaskResponse)
        async def get_one(task_id: int):
            task = self.service.get_task(task_id)
            if not task:
                raise HTTPException(404, "Not found")
            return TaskResponse(**task.to_dict())

        @self.router.delete("/{task_id}", status_code=204)
        async def delete(task_id: int):
            if not self.service.delete_task(task_id):
                raise HTTPException(404, "Not found")
