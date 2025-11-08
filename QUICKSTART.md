# Quick Start Guide

## Phase 1 Complete! 🎉

You now have a fully working Architecture Patterns Playground with:

### ✅ What's Built

1. **Monolith Task Manager API** (sample-app/01-monolith/)
   - FastAPI REST API with 6 endpoints
   - SQLite database
   - In-memory caching
   - Full test suite (all passing)

2. **Learning Platform** (platform/)
   - Beautiful responsive homepage
   - Architecture detail pages
   - Comparison view
   - Tailwind CSS styling

3. **Documentation**
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

### 4. Test the Monolith

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
├── sample-app/
│   ├── shared/domain/          # Shared domain models
│   │   ├── task.py
│   │   ├── user.py
│   │   └── project.py
│   │
│   └── 01-monolith/            # Monolith implementation (Port 8001)
│       ├── app.py              # FastAPI app
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

### Monolith API Features
- ✅ Create, Read, Update, Delete tasks
- ✅ Filter tasks by user
- ✅ Update status separately
- ✅ Tag support
- ✅ Due date tracking
- ✅ Automatic timestamps
- ✅ Caching with 60s TTL
- ✅ Comprehensive error handling
- ✅ Full test coverage

### Platform Features
- ✅ Responsive design (mobile-friendly)
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
2. **Try the API** (localhost:8001/docs) to see Swagger UI
3. **Read ADR-001** to understand architectural thinking
4. **Study the CALM spec** to learn architecture documentation
5. **Run the tests** to see how everything works

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8001
lsof -ti:8001 | xargs kill -9
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
