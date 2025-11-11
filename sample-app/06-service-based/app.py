"""Service-Based Architecture - Task Manager.

Coarse-grained services sharing a database.
Services are larger than microservices but smaller than monolith.
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority
from task_service.service import TaskServiceLogic
from shared.database import SharedDatabase


# Initialize shared database
db = SharedDatabase()

# Initialize services
task_service_logic = TaskServiceLogic(db)


# Pydantic Models
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


# FastAPI App
app = FastAPI(title="Service-Based Architecture", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])


@app.get("/")
async def root():
    return {
        "message": "Service-Based Architecture",
        "architecture": "service-based",
        "services": ["Task Service", "User Service (placeholder)", "Project Service (placeholder)"],
        "database": "Shared database across services"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}


# Task Service Endpoints
@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task_data: TaskCreate):
    task = Task(**task_data.dict())
    created = task_service_logic.create_task(task)
    return TaskResponse(**created.to_dict())

@app.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(user_id: Optional[int] = Query(None)):
    tasks = task_service_logic.get_tasks(user_id)
    return [TaskResponse(**t.to_dict()) for t in tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    task = task_service_logic.get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return TaskResponse(**task.to_dict())

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskCreate):
    existing = task_service_logic.get_task(task_id)
    if not existing:
        raise HTTPException(404, "Task not found")
    task = Task(id=task_id, created_at=existing.created_at, **task_data.dict())
    updated = task_service_logic.update_task(task_id, task)
    return TaskResponse(**updated.to_dict())

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    if not task_service_logic.delete_task(task_id):
        raise HTTPException(404, "Task not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8007)))
