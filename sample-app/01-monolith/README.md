# Monolithic Task Manager

A simple monolithic implementation of the Task Manager application using FastAPI and SQLite.

## Architecture Overview

This is a **monolithic** architecture where all components (API, business logic, and data access) are bundled into a single application.

### Characteristics

- **Single Deployment Unit**: Everything runs in one process
- **Shared Database**: All features access the same SQLite database
- **In-Memory Caching**: Simple cache for frequently accessed data
- **Synchronous Communication**: Direct function calls between components
- **CORS-Enabled**: Allows connections from Task Manager UI (port 9000)

### Pros

✅ Simple to develop and test
✅ Easy to deploy (single artifact)
✅ Straightforward debugging
✅ No network latency between components
✅ ACID transactions are simple

### Cons

❌ Tight coupling between components
❌ Difficult to scale specific features independently
❌ All components must use the same tech stack
❌ Large codebase can become hard to manage
❌ Deployment requires restarting entire application

## API Endpoints

### Tasks

- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks (optional `?user_id=` filter)
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `PATCH /tasks/{task_id}/status` - Update task status only
- `DELETE /tasks/{task_id}` - Delete a task

### Health

- `GET /` - API information
- `GET /health` - Health check

## Running Locally

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the application
python app.py

# Or use uvicorn directly
uvicorn app:app --reload --port 8001
```

The API will be available at `http://localhost:8001`

**Swagger UI**: Visit `http://localhost:8001/docs` for interactive API documentation

## Using with Task Manager UI

This API is designed to work with the **Interactive Task Manager UI** (port 9000).

```bash
# 1. Start this API (in one terminal)
python app.py

# 2. Start the Task Manager UI (in another terminal)
cd ../../task-manager-ui
python server.py

# 3. Visit http://localhost:9000 and select "Monolithic" from the dropdown
```

The API includes CORS configuration to allow requests from the UI on port 9000.

## Example Usage (via curl)

```bash
# Create a task
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build monolith",
    "description": "Implement the monolithic architecture",
    "user_id": 1,
    "project_id": 1,
    "priority": "high",
    "tags": ["architecture", "backend"]
  }'

# Get all tasks
curl http://localhost:8001/tasks

# Get tasks for a specific user
curl http://localhost:8001/tasks?user_id=1

# Update task status
curl -X PATCH http://localhost:8001/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

## Database Schema

### Tasks Table

```sql
CREATE TABLE tasks (
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
```

## Caching Strategy

Simple in-memory caching with 60-second TTL for task lists. Cache is invalidated on any write operation (create, update, delete).

## When to Use This Pattern

Choose a monolithic architecture when:

- Starting a new project with unclear requirements
- Team is small and co-located
- Application domain is simple and well-understood
- Fast iteration and development speed are priorities
- Deployment complexity needs to be minimal
