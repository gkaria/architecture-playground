# Quick Start Guide

## Phase 1 Complete! 🎉

You now have a fully working Architecture Patterns Playground with:

### ✅ What's Built

1. **Interactive Task Manager UI** (task-manager-ui/) 🎯 NEW!
   - Common frontend for all architectures
   - Architecture selector dropdown
   - Real-time performance metrics
   - Full CRUD operations with live updates
   - Filter, search, and statistics

2. **Monolith Task Manager API** (sample-app/01-monolith/)
   - FastAPI REST API with 6 endpoints
   - SQLite database
   - In-memory caching
   - CORS-enabled for UI integration
   - Full test suite (all passing)

3. **Learning Platform** (platform/)
   - Beautiful responsive homepage
   - Interactive demo link
   - Architecture detail pages
   - Comparison view
   - Tailwind CSS styling

4. **Documentation**
   - CALM specification (JSON)
   - ADR-001 (Architecture Decision Record)
   - Comprehensive READMEs

---

## Running Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Learning Platform

```bash
cd platform
python app.py
```

Visit: **http://localhost:8000**

### 3. Run the Monolith API

```bash
cd sample-app/01-monolith
python app.py
```

Visit: **http://localhost:8001/docs** for API documentation

### 4. Run the Interactive Task Manager UI 🎯 NEW!

In a new terminal window:

```bash
cd task-manager-ui
python server.py
```

Visit: **http://localhost:9000** to use the interactive demo

**Features:**
- Create, update, delete tasks with a beautiful UI
- Switch between different backend architectures
- See real-time response times
- Filter tasks by status
- Live statistics dashboard

### 5. Test the Monolith

```bash
cd sample-app/01-monolith
python test_api.py
```

---

## Try the API

### Create a Task

```bash
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Architecture Patterns",
    "description": "Study different architectural styles",
    "user_id": 1,
    "project_id": 1,
    "priority": "high",
    "tags": ["learning", "architecture"]
  }'
```

### Get All Tasks

```bash
curl http://localhost:8001/tasks
```

### Update Task Status

```bash
curl -X PATCH http://localhost:8001/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

---

## File Structure

```
architecture-playground/
├── platform/                    # Learning platform (Port 8000)
│   ├── app.py
│   └── templates/
│       ├── home.html
│       ├── architecture_detail.html
│       └── comparison.html
│
├── task-manager-ui/            # 🎯 Interactive Task Manager (Port 9000)
│   ├── index.html              # Main UI
│   ├── app.js                  # JavaScript app
│   ├── server.py               # Web server
│   └── README.md
│
├── sample-app/
│   ├── shared/domain/          # Shared domain models
│   │   ├── task.py
│   │   ├── user.py
│   │   └── project.py
│   │
│   └── 01-monolith/            # Monolith implementation (Port 8001)
│       ├── app.py              # FastAPI app (CORS-enabled)
│       ├── database.py         # SQLite operations
│       ├── test_api.py         # Test suite
│       └── README.md
│
├── calm-specs/                 # CALM documentation
│   └── monolith/
│       └── architecture.json
│
└── docs/
    └── ADRs/
        └── ADR-001-monolithic-architecture.md
```

---

## Next Steps for Phase 2

1. **Modular Monolith**
   - Add clear module boundaries
   - Create internal interfaces
   - Show how to organize a growing codebase

2. **Enhanced Platform**
   - Add code examples
   - Interactive comparisons
   - Architecture diagrams

3. **Deployment**
   - Create Render.com deployment configs
   - Set up CI/CD
   - Add monitoring

---

## Key Features

### Task Manager UI Features 🎯 NEW!
- ✅ **Architecture Selector** - Switch between backends with dropdown
- ✅ **Performance Metrics** - Real-time response time tracking
- ✅ **Full Task Management** - Create, update, delete, filter tasks
- ✅ **Live Statistics** - Total, In Progress, Done counts
- ✅ **Beautiful UI** - Modern, responsive design with Tailwind CSS
- ✅ **Status Updates** - Quick status changes via dropdown
- ✅ **Tag Support** - Add and display task tags
- ✅ **Priority Levels** - Low, Medium, High priorities
- ✅ **Error Handling** - Graceful failures with retry options

### Monolith API Features
- ✅ Create, Read, Update, Delete tasks
- ✅ Filter tasks by user
- ✅ Update status separately
- ✅ Tag support
- ✅ Due date tracking
- ✅ Automatic timestamps
- ✅ Caching with 60s TTL
- ✅ CORS-enabled for UI integration
- ✅ Comprehensive error handling
- ✅ Full test coverage

### Platform Features
- ✅ Responsive design (mobile-friendly)
- ✅ Interactive demo link (prominent CTA)
- ✅ 6 architecture pattern cards
- ✅ Detailed pattern explanations
- ✅ Trade-off analysis
- ✅ Side-by-side comparisons
- ✅ CALM spec viewer

### Documentation Features
- ✅ FINOS CALM specification
- ✅ Architecture Decision Records
- ✅ Pattern-specific guides
- ✅ Quick start instructions
- ✅ Task Manager UI documentation

---

## Learning Resources

### Explore the CALM Spec
```bash
cat calm-specs/monolith/architecture.json | python -m json.tool
```

### Read the ADR
```bash
cat docs/ADRs/ADR-001-monolithic-architecture.md
```

### Study the Domain Models
```bash
cat sample-app/shared/domain/task.py
```

---

## Tips

1. **Start with the platform** (localhost:8000) to see the big picture
2. **Try the interactive demo** (localhost:9000) to experience the UI 🎯 NEW!
3. **Explore the API** (localhost:8001/docs) to see Swagger UI documentation
4. **Read ADR-001** to understand architectural thinking
5. **Study the CALM spec** to learn architecture documentation
6. **Run the tests** to see how everything works
7. **Switch architectures** in the Task Manager UI to see performance differences

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000 (Learning Platform)
lsof -ti:8000 | xargs kill -9

# Kill process on port 8001 (Monolith API)
lsof -ti:8001 | xargs kill -9

# Kill process on port 9000 (Task Manager UI)
lsof -ti:9000 | xargs kill -9
```

### Database Issues
```bash
# Remove old database
rm sample-app/01-monolith/tasks.db

# Restart the app (it will recreate the DB)
```

### Import Errors
```bash
# Make sure you're in the right directory
cd /home/user/architecture-playground

# Install dependencies
pip install -r requirements.txt
```

---

## What's Next?

Phase 1 is **COMPLETE** and ready to deploy!

You can now:
1. Deploy to Render.com
2. Share your portfolio project
3. Start building Phase 2 (Modular Monolith)
4. Add more features to the platform

**Congratulations on building a production-ready learning platform!** 🎉
