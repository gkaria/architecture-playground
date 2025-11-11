# Architecture Patterns Playground - AI Coding Agent Instructions

## Project Overview

**Architecture Patterns Playground** is an educational portfolio project that demonstrates how the same Task Manager application can be implemented using 6 different architectural patterns (Monolith, Modular Monolith, Microservices, Event-Driven, Layered, Service-Based).

**Key Goal**: Help developers understand trade-offs between architectural patterns through working implementations and interactive comparison tools.

---

## Critical Architecture & Data Flows

### Multi-Service Architecture

The project has **3 distinct services** running on different ports:

1. **Learning Platform** (`platform/app.py`, Port 8000)
   - Server-side rendered FastAPI app with Jinja2 templates
   - Serves static Tailwind CSS via CDN
   - Role: Educational homepage, pattern explanations, comparison views
   - Routes environment URLs to UI and API services

2. **Monolith API** (`sample-app/01-monolith/app.py`, Port 8001)
   - FastAPI REST API (6 CRUD endpoints for tasks)
   - SQLite database (tasks.db)
   - In-memory cache (60s TTL for /tasks queries)
   - CORS-enabled for UI integration
   - Rate limiting: 100/min (reads), 30/min (writes), 20/min (creates)

3. **Task Manager UI** (`task-manager-ui/server.py`, Port 9000)
   - Frontend with vanilla JavaScript (no frameworks)
   - Architecture selector dropdown for switching backends
   - Dynamic API URL detection (localhost in dev, production URLs in prod)
   - Connects to monolith API for task operations

### Data Flow Patterns

- **UI → API**: Form submissions and CRUD operations flow through REST endpoints
- **Caching**: Database queries on `/tasks` are cached; cache invalidates on create/update/delete
- **CORS**: Configured via `security.get_cors_config()` - restrictive whitelist (no wildcards)
- **Input Flow**: All user inputs sanitized via `bleach` library → prevent XSS → stored to SQLite

---

## Shared Domain Model (Critical to All Architectures)

Located in `sample-app/shared/domain/`:

```python
# task.py: TaskStatus (enum: todo/in_progress/done), TaskPriority (low/medium/high)
# user.py, project.py: Other entities (not yet fully used)

# Task model attributes: id, title, description, status, priority, user_id, project_id, 
#                       created_at, updated_at, due_date, tags
# Methods: to_dict(), from_dict() for serialization across boundaries
```

**Important**: All 6 architecture implementations share this exact domain model. When adding new patterns, **reuse these classes unchanged** to ensure fair comparison.

---

## Key Developer Workflows

### Running All Services (Development)

```bash
# Terminal 1: Learning Platform
cd platform && python app.py

# Terminal 2: Monolith API
cd sample-app/01-monolith && python app.py

# Terminal 3: Task Manager UI
cd task-manager-ui && python server.py

# Then visit: http://localhost:8000
```

### Testing

```bash
# Run monolith tests
cd sample-app/01-monolith
python test_api.py  # Simple script-based tests, not pytest

# Key test patterns:
# - Create task first, then get/update/delete
# - Use TestClient from fastapi.testclient
# - Tests are simple and educational (not comprehensive)
```

### Deployment (Render.com)

- `render.yaml` in root: Auto-detects all services via blueprints
- Environment variables (set by render.yaml):
  - `API_URL`: Production API base URL (platform uses this)
  - `UI_URL`: Production UI URL (platform uses this)
  - `CORS_ORIGINS`: Comma-separated list for backend CORS
- Auto-deploys on git push (if `autoDeploy: true`)
- Free tier: 750 hours/month, cold starts after 15 min inactivity

---

## Project Patterns & Conventions

### API Endpoint Design

**Monolith pattern** (to replicate in other architectures):
- `POST /tasks` - Create (uses Pydantic TaskCreate model)
- `GET /tasks` - List all (with optional `?user_id=X` filter)
- `GET /tasks/{id}` - Get single task
- `PUT /tasks/{id}` - Full update
- `PATCH /tasks/{id}/status` - Status-only update
- `DELETE /tasks/{id}` - Delete
- `GET /health` - Health check

**Rate limit decorators** applied to every endpoint using `@limiter.limit()`.

### Security Conventions

1. **Input Sanitization** (`security.sanitize_string()`):
   - Uses bleach library to strip all HTML tags
   - Enforces max_length parameter
   - Applied to: title (200 chars), description (2000 chars), tags (50 chars)

2. **CORS Configuration** (dynamic):
   - Dev: localhost:8000, localhost:8001, localhost:9000
   - Prod: Uses `CORS_ORIGINS` env var (set in render.yaml)
   - Never use wildcard `*` - this project uses restrictive allowlist

3. **Rate Limiting Constants**:
   ```python
   RATE_LIMIT_READ = "100/minute"
   RATE_LIMIT_WRITE = "30/minute"
   RATE_LIMIT_CREATE = "20/minute"
   ```

### Database Pattern (SQLite)

- Context manager pattern: `with self.get_connection() as conn:`
- Always use parameterized queries: `cursor.execute("...", (params,))`
- Row conversion: `_row_to_task()` converts sqlite3.Row → Task domain object
- Transactions: Automatic commit on success, rollback on exception
- **Important**: Timestamps stored as ISO format strings, converted on retrieval

### Caching Pattern (In-Memory)

```python
# Cache key structure: "tasks_all" or "tasks_{user_id}"
# Cache entry: (timestamp, data)
# TTL: 60 seconds
# Invalidation: On any write operation
```

### Frontend Architecture (Vanilla JS)

- No frameworks (keep it simple for learning)
- Architecture selector: Changes `currentArchitecture` → Re-fetches from new API
- Dynamic URL detection: `getApiUrl()` returns localhost in dev, production URLs when deployed
- UI Updates: DOM manipulation via `document.getElementById()` and template strings
- State management: Simple global variables (`tasks`, `currentArchitecture`, `currentFilter`)

---

## Cross-Component Integration Points

### Platform ↔ Monolith API

- Platform calls `/calm/{arch_id}` to load architecture specs from `calm-specs/` directory
- Platform reads `ARCHITECTURES` config to populate cards and links
- Platform redirects to UI at `http://localhost:9000` (dev) or env var (prod)

### UI ↔ Monolith API

- UI auto-detects environment and builds API URL via `getApiUrl()`
- UI sends all task operations as REST JSON (no multipart, no GraphQL)
- CORS headers validated by API via `CORSMiddleware` config
- Performance metrics: UI measures response times for each API call

### Monolith API ↔ Database

- Database initialization: `Database().init_db()` creates schema on first connection
- Connection pooling: Basic via context manager (no external pool library)
- Schema: 3 tables (tasks, users, projects) - users/projects mostly stubbed out

---

## Key Files & Their Responsibilities

| File | Purpose | When to Modify |
|------|---------|----------------|
| `sample-app/shared/domain/*` | Shared models used by all architectures | When adding Task fields across all patterns |
| `sample-app/01-monolith/app.py` | Monolith API implementation (template for others) | When fixing endpoints or adding new operations |
| `sample-app/01-monolith/database.py` | SQLite operations | When changing persistence layer |
| `sample-app/01-monolith/security.py` | Rate limiting, CORS, input sanitization | When adjusting security rules |
| `platform/app.py` | Learning platform routes & data | When adding new pattern explanations |
| `task-manager-ui/app.js` | Frontend state management & API calls | When changing UI behavior or switching architecture logic |
| `requirements.txt` | Python dependencies | When adding new libraries (must install in all architecture dirs) |
| `render.yaml` | Deployment configuration | When modifying services or ports |
| `calm-specs/monolith/architecture.json` | CALM documentation (machine-readable spec) | When documenting architecture decisions |
| `docs/ADRs/ADR-001-*.md` | Architecture Decision Records | When explaining architectural choices |

---

## Common Tasks & Patterns

### Adding a New Endpoint to Monolith

1. Add endpoint in `app.py` with decorators:
   ```python
   @app.post("/new-endpoint")
   @limiter.limit(RATE_LIMIT_WRITE)
   async def endpoint(request: Request, data: PydanticModel):
       # Implementation
   ```

2. Add corresponding method to `Database` class in `database.py`
3. Add test case to `test_api.py`
4. Invalidate cache if needed: `invalidate_cache()`

### Adding a New Architecture Implementation

1. Create `sample-app/{02,03,04,05,06}-{pattern}/` directory
2. Copy `sample-app/01-monolith/` as template:
   - `app.py`: Implement same 6 endpoints using pattern-specific approach
   - `database.py`: Implement persistence for this architecture
   - `security.py`: Reuse or modify based on pattern needs
   - `test_api.py`: Test endpoints
   - `README.md`: Explain this pattern's design
3. Update `task-manager-ui/app.js` ARCHITECTURES config with new port
4. Update `platform/app.py` ARCHITECTURES list (change `status` from "coming_soon")
5. Create `calm-specs/{pattern}/architecture.json` with CALM spec
6. Update `render.yaml` to add new service

### Modifying UI to Support New Architecture

1. Add to `ARCHITECTURES` object in `task-manager-ui/app.js`:
   ```javascript
   'new-pattern': {
       port: 8007,
       color: 'orange',
       name: 'New Pattern',
       prodUrl: 'https://...'
   }
   ```
2. Add corresponding prod URL to backend CORS whitelist
3. Test architecture selector dropdown

---

## Important Non-Standard Patterns

1. **No ORM** - Raw SQLite with manual SQL and Row → Object conversion
2. **Simple Testing** - `test_api.py` is a script not pytest (educational, simple to understand)
3. **Cache Invalidation** - On any write, cache is completely cleared (not sophisticated)
4. **No async database** - SQLite operations are synchronous despite FastAPI being async
5. **Timestamps as ISO strings** - Stored and retrieved as string, not UNIX timestamp
6. **Enum serialization** - TaskStatus/Priority enums are string-based (Enum inherits str)

---

## Deployment Context

- **Free Tier Limitations**: 30-60 second cold starts, services sleep after 15 min inactivity
- **Ephemeral Disk**: SQLite database resets on service restart (data loss on redeploy)
- **Auto-Deploy**: Any git push to main triggers rebuild on all services
- **Production URLs**: All 3 services have dedicated Render.com URLs (hardcoded in UI)
- **Database Upgrade Path**: Document recommends PostgreSQL for future iterations

---

## Documentation Sources

- **Architecture Overview**: `README.md` (comprehensive), `QUICKSTART.md` (getting started)
- **Deployment Guide**: `DEPLOYMENT.md` (render.yaml config, free tier notes)
- **Design Rationale**: `docs/ADRs/ADR-001-monolithic-architecture.md`
- **Machine-Readable Spec**: `calm-specs/monolith/architecture.json` (FINOS CALM format)

---

## Red Flags & Gotchas

1. **Cache Stampedes**: Cache clearing on every write is simplistic (not a production pattern)
2. **SQLite Concurrency**: Not suitable for high-concurrency scenarios
3. **Data Persistence**: Free tier Render.com doesn't persist data - each deploy creates new DB
4. **CORS Debugging**: Check `security.get_cors_origins()` - dev vs prod behavior differs
5. **Rate Limiting**: Based on IP address - may be problematic behind proxies
6. **Missing Auth**: No authentication/authorization (educational only, security module is basic)

---

## When to Ask for Clarification

- Schema or API contract changes across multiple architectures (ensure consistency)
- New external dependencies (update `requirements.txt` in all relevant architecture dirs)
- Deployment configuration changes (affects `render.yaml` blueprint)
- Domain model changes (shared across all patterns)
- Database migration strategy (SQLite limitations make this tricky)
