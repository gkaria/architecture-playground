"""Layered Architecture - Task Manager.

Traditional layered architecture with:
- Presentation Layer: API endpoints
- Business Layer: Business logic
- Data Layer: Database access

Each layer only communicates with the layer below it.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).parent.parent.parent))
from shared.domain import Task, TaskStatus, TaskPriority

# Import layers
from data.task_repository import TaskRepository
from business.task_service import TaskService
from presentation.task_controller import TaskController


# Initialize layers
repository = TaskRepository()
service = TaskService(repository)
controller = TaskController(service)

# FastAPI App
app = FastAPI(title="Layered Architecture Task Manager", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Layered Architecture", "architecture": "layered",
            "layers": ["Presentation", "Business", "Data"]}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Register presentation layer routes
app.include_router(controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8005)))
