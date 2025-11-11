"""Task Service - Microservices Architecture.

Independent service responsible for task management operations.
Has its own database and can be deployed/scaled independently.
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pathlib import Path
import sys
import os
import sqlite3
import json
from contextlib import contextmanager
import bleach
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority


# Security utilities
limiter = Limiter(key_func=get_remote_address)
RATE_LIMIT_READ = "100/minute"
RATE_LIMIT_WRITE = "30/minute"
RATE_LIMIT_CREATE = "20/minute"


def sanitize_string(text: str, max_length: int = 2000) -> str:
    """Sanitize user input."""
    if not text:
        return text
    text = text[:max_length]
    return bleach.clean(text, tags=[], strip=True).strip()


def sanitize_tags(tags: list[str]) -> list[str]:
    """Sanitize tags."""
    if not tags:
        return []
    return [sanitize_string(tag, 50) for tag in tags if tag]


# Database class for Task Service
class TaskDatabase:
    """Database manager for task service."""

    def __init__(self, db_path: str = "task_service.db"):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    project_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    due_date TEXT,
                    tags TEXT
                )
            """)

    def create_task(self, task: Task) -> Task:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (
                    title, description, status, priority,
                    user_id, project_id, created_at, updated_at,
                    due_date, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.title, task.description,
                task.status.value, task.priority.value,
                task.user_id, task.project_id,
                task.created_at.isoformat(), task.updated_at.isoformat(),
                task.due_date.isoformat() if task.due_date else None,
                json.dumps(task.tags)
            ))
            task.id = cursor.lastrowid
            return task

    def get_task(self, task_id: int) -> Optional[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return self._row_to_task(row) if row else None

    def get_tasks(self, user_id: Optional[int] = None) -> list[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if user_id is not None:
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            return [self._row_to_task(row) for row in rows]

    def update_task(self, task_id: int, task: Task) -> Optional[Task]:
        task.updated_at = datetime.utcnow()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET
                    title = ?, description = ?, status = ?, priority = ?,
                    user_id = ?, project_id = ?, updated_at = ?,
                    due_date = ?, tags = ?
                WHERE id = ?
            """, (
                task.title, task.description,
                task.status.value, task.priority.value,
                task.user_id, task.project_id,
                task.updated_at.isoformat(),
                task.due_date.isoformat() if task.due_date else None,
                json.dumps(task.tags),
                task_id
            ))
            if cursor.rowcount == 0:
                return None
            task.id = task_id
            return task

    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET status = ?, updated_at = ?
                WHERE id = ?
            """, (status.value, datetime.utcnow().isoformat(), task_id))
            if cursor.rowcount == 0:
                return None
        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    def _row_to_task(self, row) -> Task:
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=TaskStatus(row["status"]),
            priority=TaskPriority(row["priority"]),
            user_id=row["user_id"],
            project_id=row["project_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
            tags=json.loads(row["tags"]) if row["tags"] else []
        )


# Pydantic models
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    user_id: int = Field(..., gt=0)
    project_id: int = Field(..., gt=0)
    due_date: Optional[datetime] = None
    tags: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=2000)
    status: TaskStatus
    priority: TaskPriority
    user_id: int = Field(..., gt=0)
    project_id: int = Field(..., gt=0)
    due_date: Optional[datetime] = None
    tags: list[str] = Field(default_factory=list)


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


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


# Initialize FastAPI app
app = FastAPI(
    title="Task Service",
    description="Microservice for task management",
    version="1.0.0"
)

# Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = TaskDatabase()


@app.get("/")
@limiter.limit(RATE_LIMIT_READ)
async def root(request: Request):
    return {
        "service": "Task Service",
        "version": "1.0.0",
        "architecture": "microservices",
        "type": "independent-service"
    }


@app.get("/health")
@limiter.limit(RATE_LIMIT_READ)
async def health(request: Request):
    return {"status": "healthy", "service": "task-service"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
@limiter.limit(RATE_LIMIT_CREATE)
async def create_task(request: Request, task_data: TaskCreate):
    try:
        task = Task(
            title=sanitize_string(task_data.title, 200),
            description=sanitize_string(task_data.description, 2000),
            status=task_data.status,
            priority=task_data.priority,
            user_id=task_data.user_id,
            project_id=task_data.project_id,
            due_date=task_data.due_date,
            tags=sanitize_tags(task_data.tags)
        )
        created_task = db.create_task(task)
        return TaskResponse(**created_task.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks", response_model=list[TaskResponse])
@limiter.limit(RATE_LIMIT_READ)
async def get_tasks(request: Request, user_id: Optional[int] = Query(None, gt=0)):
    try:
        tasks = db.get_tasks(user_id)
        return [TaskResponse(**task.to_dict()) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit(RATE_LIMIT_READ)
async def get_task(request: Request, task_id: int):
    try:
        task = db.get_task(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return TaskResponse(**task.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit(RATE_LIMIT_WRITE)
async def update_task(request: Request, task_id: int, task_data: TaskUpdate):
    try:
        existing_task = db.get_task(task_id)
        if existing_task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        task = Task(
            id=task_id,
            title=sanitize_string(task_data.title, 200),
            description=sanitize_string(task_data.description, 2000),
            status=task_data.status,
            priority=task_data.priority,
            user_id=task_data.user_id,
            project_id=task_data.project_id,
            created_at=existing_task.created_at,
            due_date=task_data.due_date,
            tags=sanitize_tags(task_data.tags)
        )
        updated_task = db.update_task(task_id, task)
        return TaskResponse(**updated_task.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
@limiter.limit(RATE_LIMIT_WRITE)
async def update_task_status(request: Request, task_id: int, status_data: TaskStatusUpdate):
    try:
        updated_task = db.update_task_status(task_id, status_data.status)
        if updated_task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return TaskResponse(**updated_task.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/tasks/{task_id}", status_code=204)
@limiter.limit(RATE_LIMIT_WRITE)
async def delete_task(request: Request, task_id: int):
    try:
        deleted = db.delete_task(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)
