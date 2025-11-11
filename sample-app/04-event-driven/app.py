"""Event-Driven Architecture - Task Manager.

Uses event-based communication between components.
Components communicate asynchronously through events.
"""

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Callable, Any
from pathlib import Path
import sys
import os
import sqlite3
import json
from contextlib import contextmanager
import asyncio
from collections import defaultdict

sys.path.append(str(Path(__file__).parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority


# Event Bus Implementation
class EventBus:
    """Simple in-memory event bus for async communication."""

    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event type."""
        self._handlers[event_type].append(handler)

    async def publish(self, event_type: str, data: dict):
        """Publish an event to all subscribers."""
        handlers = self._handlers.get(event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                print(f"Error in event handler: {e}")


# Global event bus
event_bus = EventBus()


# Database
class Database:
    def __init__(self, db_path: str = "event_driven.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self.get_connection() as conn:
            conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT, description TEXT, status TEXT, priority TEXT,
                    user_id INTEGER, project_id INTEGER,
                    created_at TEXT, updated_at TEXT, due_date TEXT, tags TEXT
                )
            """)

    def create_task(self, task: Task) -> Task:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, description, status, priority,
                    user_id, project_id, created_at, updated_at, due_date, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task.title, task.description, task.status.value, task.priority.value,
                  task.user_id, task.project_id, task.created_at.isoformat(),
                  task.updated_at.isoformat(),
                  task.due_date.isoformat() if task.due_date else None,
                  json.dumps(task.tags)))
            task.id = cursor.lastrowid
            return task

    def get_tasks(self, user_id: Optional[int] = None) -> list[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM tasks")
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def get_task(self, task_id: int) -> Optional[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return self._row_to_task(row) if row else None

    def update_task(self, task_id: int, task: Task) -> Optional[Task]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET title=?, description=?, status=?, priority=?,
                    user_id=?, project_id=?, updated_at=?, due_date=?, tags=?
                WHERE id=?
            """, (task.title, task.description, task.status.value, task.priority.value,
                  task.user_id, task.project_id, datetime.utcnow().isoformat(),
                  task.due_date.isoformat() if task.due_date else None,
                  json.dumps(task.tags), task_id))
            return self.get_task(task_id) if cursor.rowcount > 0 else None

    def delete_task(self, task_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    def _row_to_task(self, row) -> Task:
        return Task(
            id=row["id"], title=row["title"], description=row["description"],
            status=TaskStatus(row["status"]), priority=TaskPriority(row["priority"]),
            user_id=row["user_id"], project_id=row["project_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
            tags=json.loads(row["tags"]) if row["tags"] else []
        )


# Event Handlers
async def on_task_created(data: dict):
    """Handle task created event."""
    print(f"[EVENT] Task created: {data['task_id']}")
    # Could trigger: send notification, update analytics, etc.

async def on_task_updated(data: dict):
    """Handle task updated event."""
    print(f"[EVENT] Task updated: {data['task_id']}")

async def on_task_deleted(data: dict):
    """Handle task deleted event."""
    print(f"[EVENT] Task deleted: {data['task_id']}")


# Subscribe to events
event_bus.subscribe("task.created", on_task_created)
event_bus.subscribe("task.updated", on_task_updated)
event_bus.subscribe("task.deleted", on_task_deleted)


# Pydantic Models
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
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    user_id: int
    project_id: int
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
app = FastAPI(title="Event-Driven Task Manager", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

db = Database()


@app.get("/")
async def root():
    return {"message": "Event-Driven Task Manager", "architecture": "event-driven"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task_data: TaskCreate):
    task = Task(**task_data.dict())
    created_task = db.create_task(task)
    await event_bus.publish("task.created", {"task_id": created_task.id})
    return TaskResponse(**created_task.to_dict())

@app.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(user_id: Optional[int] = Query(None)):
    tasks = db.get_tasks(user_id)
    return [TaskResponse(**t.to_dict()) for t in tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return TaskResponse(**task.to_dict())

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskUpdate):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    updated_task = db.update_task(task_id, Task(id=task_id, created_at=task.created_at, **task_data.dict()))
    await event_bus.publish("task.updated", {"task_id": task_id})
    return TaskResponse(**updated_task.to_dict())

@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_status(task_id: int, status: TaskStatus):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task.status = status
    updated = db.update_task(task_id, task)
    await event_bus.publish("task.updated", {"task_id": task_id})
    return TaskResponse(**updated.to_dict())

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    if not db.delete_task(task_id):
        raise HTTPException(404, "Task not found")
    await event_bus.publish("task.deleted", {"task_id": task_id})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8004)))
