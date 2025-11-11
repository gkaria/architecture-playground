# Modular Monolith Implementation

This directory contains the **Modular Monolith** implementation of the Task Manager application.

## Architecture Overview

A **Modular Monolith** is an architectural pattern that combines the deployment simplicity of a monolith with the organizational benefits of modular architecture. The application is still deployed as a single unit, but the code is organized into well-defined modules with clear boundaries.

### Key Characteristics

- **Single Deployment Unit**: The entire application runs as one process
- **Module Boundaries**: Clear separation between modules (tasks, users, projects)
- **Layered Modules**: Each module has its own repository, service, and API layers
- **Shared Infrastructure**: Common infrastructure (database, security) is centralized
- **Low Coupling**: Modules communicate through well-defined interfaces

## Directory Structure

```
02-modular-monolith/
├── app.py                          # Main application - orchestrates modules
├── infrastructure/                 # Shared infrastructure
│   ├── database.py                # Database connection and base repository
│   └── security.py                # Security utilities (rate limiting, sanitization)
└── modules/                       # Application modules
    └── tasks/                     # Tasks module
        ├── repository.py          # Data access layer
        ├── service.py             # Business logic layer
        └── router.py              # API routing layer
```

## Module Architecture

Each module follows a three-layer architecture:

### 1. Repository Layer (`repository.py`)
- Handles all database operations
- Provides data access methods
- Converts between database rows and domain objects

### 2. Service Layer (`service.py`)
- Contains business logic and validation
- Orchestrates operations across repositories
- Implements caching and business rules

### 3. Router Layer (`router.py`)
- Defines REST API endpoints
- Handles HTTP request/response
- Validates input using Pydantic models

## Running the Application

### Start the server:
```bash
cd sample-app/02-modular-monolith
python app.py
```

The API will be available at `http://localhost:8002`

### Run with custom port:
```bash
PORT=8002 python app.py
```

## API Endpoints

All endpoints are identical to the monolith implementation:

- `GET /` - API information
- `GET /health` - Health check
- `POST /tasks` - Create a task
- `GET /tasks` - List all tasks (optional `?user_id=` filter)
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `PATCH /tasks/{id}/status` - Update task status only
- `DELETE /tasks/{id}` - Delete a task

## Comparison with Monolith

| Aspect | Monolith | Modular Monolith |
|--------|----------|------------------|
| **Deployment** | Single unit | Single unit |
| **Code Organization** | All in one file | Organized into modules |
| **Testability** | Test entire app | Test modules independently |
| **Maintainability** | Lower | Higher |
| **Team Scalability** | Limited | Better - teams can own modules |
| **Performance** | Fast | Fast (same process) |
| **Complexity** | Low | Medium |

## Advantages

1. **Better Organization**: Clear module boundaries make code easier to understand
2. **Independent Testing**: Modules can be tested in isolation
3. **Team Scalability**: Different teams can work on different modules
4. **Refactoring Path**: Easy to extract modules into microservices later
5. **Single Deployment**: Simpler deployment than microservices

## Disadvantages

1. **Architectural Discipline Required**: Developers must maintain module boundaries
2. **Shared Database**: All modules share the same database
3. **Coupled Deployment**: All modules deploy together
4. **Resource Scaling**: Cannot scale individual modules independently

## When to Use

- **Medium-sized applications** that need better organization than a monolith
- **Growing teams** that need to work independently on different features
- **Applications** that may evolve into microservices later
- **Projects** where deployment simplicity is important

## Migration Path

This architecture provides a natural migration path:

1. **Start**: Traditional monolith (Phase 1)
2. **Organize**: Modular monolith with clear boundaries (Phase 2) ← **You are here**
3. **Extract**: Microservices by extracting modules (Phase 3)

## Security Features

- **Rate Limiting**: Prevents API abuse
  - 100 req/min for read operations
  - 30 req/min for write operations
  - 20 req/min for create operations
- **Input Sanitization**: Prevents XSS attacks
- **CORS Configuration**: Restricts cross-origin requests

## Database

- **Type**: SQLite (same as monolith)
- **File**: `modular_tasks.db`
- **Schema**: Identical to monolith (tasks, users, projects tables)
- **Access**: Through repository layer only

## Testing

Each module can be tested independently:

```python
# Test repository layer
task_repo = TaskRepository(test_db)
task = task_repo.create(test_task)

# Test service layer
task_service = TaskService(mock_repository)
result = task_service.create_task(task_data)

# Test API layer
response = client.post("/tasks", json=task_data)
```

## Future Enhancements

- Add Users module with similar structure
- Add Projects module with similar structure
- Implement inter-module communication patterns
- Add module-level caching strategies
- Implement module-level monitoring
