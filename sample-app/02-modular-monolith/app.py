"""Modular Monolith Task Manager FastAPI application.

This implementation demonstrates a modular monolith architecture where:
- The application is still a single deployment unit
- Code is organized into well-defined modules (tasks, users, projects)
- Each module has clear boundaries and responsibilities
- Modules communicate through well-defined interfaces
- Shared infrastructure (database, security) is centralized
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import os

from infrastructure.database import DatabaseConnection
from infrastructure.security import limiter, get_cors_config, RATE_LIMIT_READ

# Import module components
from modules.tasks.repository import TaskRepository
from modules.tasks.service import TaskService
from modules.tasks.router import create_task_router


# Initialize FastAPI app
app = FastAPI(
    title="Task Manager Modular Monolith",
    description="A modular monolith implementation with clear module boundaries",
    version="1.0.0"
)

# Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
cors_config = get_cors_config()
app.add_middleware(CORSMiddleware, **cors_config)

# Initialize shared infrastructure
db_connection = DatabaseConnection()

# Initialize modules
# Tasks Module
task_repository = TaskRepository(db_connection)
task_service = TaskService(task_repository)
task_router = create_task_router(task_service)

# Register module routers
app.include_router(task_router)


@app.get("/")
@limiter.limit(RATE_LIMIT_READ)
async def root(request: Request):
    """Root endpoint."""
    return {
        "message": "Task Manager Modular Monolith API",
        "version": "1.0.0",
        "architecture": "modular-monolith",
        "modules": {
            "tasks": "Task management module with repository, service, and API layers",
            "users": "User management module (placeholder)",
            "projects": "Project management module (placeholder)"
        },
        "architectural_characteristics": {
            "deployment": "Single deployment unit",
            "modularity": "High - clear module boundaries",
            "coupling": "Low - modules communicate through interfaces",
            "testability": "High - modules can be tested independently"
        }
    }


@app.get("/health")
@limiter.limit(RATE_LIMIT_READ)
async def health_check(request: Request):
    """Health check endpoint."""
    return {
        "status": "healthy",
        "architecture": "modular-monolith",
        "modules_loaded": ["tasks"]
    }


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
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
