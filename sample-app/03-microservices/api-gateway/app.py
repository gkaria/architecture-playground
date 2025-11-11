"""API Gateway - Microservices Architecture.

Routes requests to appropriate microservices.
Provides a single entry point for the frontend.
"""

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
from typing import Optional

# Service URLs (configurable via environment variables)
TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://localhost:8003")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8004")
PROJECT_SERVICE_URL = os.getenv("PROJECT_SERVICE_URL", "http://localhost:8005")

# Initialize FastAPI app
app = FastAPI(
    title="API Gateway",
    description="Gateway routing requests to microservices",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def forward_request(
    service_url: str,
    path: str,
    method: str,
    request: Request,
    body: Optional[bytes] = None
) -> Response:
    """Forward request to a microservice.

    Args:
        service_url: Base URL of the service
        path: Path to forward to
        method: HTTP method
        request: Original request
        body: Request body

    Returns:
        Response from the service
    """
    url = f"{service_url}{path}"
    headers = dict(request.headers)
    # Remove host header to avoid conflicts
    headers.pop("host", None)

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=body,
                params=dict(request.query_params)
            )

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type")
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail=f"Service unavailable: {service_url}"
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail=f"Service timeout: {service_url}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Gateway error: {str(e)}"
            )


@app.get("/")
async def root():
    """Gateway information."""
    return {
        "service": "API Gateway",
        "version": "1.0.0",
        "architecture": "microservices",
        "services": {
            "tasks": TASK_SERVICE_URL,
            "users": USER_SERVICE_URL,
            "projects": PROJECT_SERVICE_URL
        }
    }


@app.get("/health")
async def health():
    """Health check for gateway."""
    services_health = {}

    async with httpx.AsyncClient(timeout=5.0) as client:
        # Check task service
        try:
            response = await client.get(f"{TASK_SERVICE_URL}/health")
            services_health["task-service"] = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception:
            services_health["task-service"] = "unreachable"

    return {
        "gateway": "healthy",
        "services": services_health
    }


# Task service routes
@app.api_route("/tasks", methods=["GET", "POST"])
async def tasks_route(request: Request):
    """Route to task service."""
    body = await request.body() if request.method == "POST" else None
    return await forward_request(
        TASK_SERVICE_URL,
        "/tasks",
        request.method,
        request,
        body
    )


@app.api_route("/tasks/{task_id}", methods=["GET", "PUT", "PATCH", "DELETE"])
async def task_by_id_route(request: Request, task_id: int):
    """Route to task service for specific task."""
    body = await request.body() if request.method in ["PUT", "PATCH"] else None
    return await forward_request(
        TASK_SERVICE_URL,
        f"/tasks/{task_id}",
        request.method,
        request,
        body
    )


@app.api_route("/tasks/{task_id}/status", methods=["PATCH"])
async def task_status_route(request: Request, task_id: int):
    """Route to task service for status update."""
    body = await request.body()
    return await forward_request(
        TASK_SERVICE_URL,
        f"/tasks/{task_id}/status",
        request.method,
        request,
        body
    )


# User service routes (placeholder - service not implemented yet)
@app.api_route("/users", methods=["GET", "POST"])
async def users_route(request: Request):
    """Route to user service (placeholder)."""
    return JSONResponse(
        status_code=501,
        content={"detail": "User service not implemented yet"}
    )


# Project service routes (placeholder - service not implemented yet)
@app.api_route("/projects", methods=["GET", "POST"])
async def projects_route(request: Request):
    """Route to project service (placeholder)."""
    return JSONResponse(
        status_code=501,
        content={"detail": "Project service not implemented yet"}
    )


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
    port = int(os.getenv("PORT", 8006))
    uvicorn.run(app, host="0.0.0.0", port=port)
