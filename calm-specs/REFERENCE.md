# CALM Architecture Quick Reference

## 📁 File Location
```
calm-specs/system.architecture.json
```

## 🔍 Viewing the Architecture

### Pretty Print the JSON
```bash
cat system.architecture.json | python -m json.tool
```

### Validate the Architecture
```bash
calm validate -a system.architecture.json
```

### View Specific Sections
```bash
# View all nodes
cat system.architecture.json | python -m json.tool | grep -A 5 '"unique-id"'

# View all relationships  
cat system.architecture.json | python -m json.tool | grep -A 10 '"relationship-type"'

# View all flows
cat system.architecture.json | python -m json.tool | grep -A 15 '"transitions"'
```

## 📊 Architecture Statistics

| Component | Count | Details |
|-----------|-------|---------|
| **Nodes** | 9 | 2 actors, 2 services, 1 webclient, 1 database, 3 data assets |
| **Relationships** | 11 | 4 business interactions, 7 technical connections |
| **Flows** | 3 | 1 learning flow, 1 creation flow, 1 retrieval flow |
| **Controls** | 5 | Security & reliability requirements |
| **Interfaces** | 5 | HTTP (2x), JDBC (1x), JSON (2x implicit) |

## 🎯 Key Nodes

### Services
```json
{
  "learning-platform": "Port 8000 - Educational platform",
  "monolith-api": "Port 8001 - REST API backend"
}
```

### Frontend
```json
{
  "task-manager-ui": "Port 9000 - Vanilla JS UI"
}
```

### Storage
```json
{
  "monolith-database": "SQLite (tasks.db)"
}
```

## 🔗 Key Relationships

**Data Flow**:
```
Browser → Learning Platform → CALM Specs
         ↓
      Task Manager UI → Monolith API → SQLite Database
```

**Domain Models**:
```
Shared Models ← Monolith API
             ← Documentation
```

## 📋 Flows at a Glance

### Developer Learning Flow (7 steps)
1. Opens browser → 2. Views homepage → 3. Reads CALM specs → 4. Reviews ADRs 
→ 5. Accesses UI → 6. Loads task manager → 7. Connects to API

### Task Creation Flow (6 steps)  
1. Form submit → 2. REST API call → 3. Domain validation → 4. DB insert 
→ 5. Response returned → 6. UI updated

### Task Retrieval Flow (6 steps)
1. Load tasks → 2. API GET request → 3. Cache check → 4. DB query (if miss)
→ 5. Return data → 6. Render UI

## 🔒 Security Controls

| Control | Type | Implementation |
|---------|------|-----------------|
| Input Sanitization | Security | `bleach` library strips HTML |
| Rate Limiting | Security | 100/min read, 30/min write, 20/min create |
| CORS Policy | Security | Restrictive whitelist (no wildcards) |
| Parameterized Queries | Security | SQL injection prevention |
| Transaction Rollback | Reliability | Auto-rollback on errors |

## 📐 Node Types Used

- **actor** - External entity (developer, browser)
- **service** - Business logic components (learning platform, API)
- **webclient** - Frontend (task manager UI)
- **database** - Data storage (SQLite)
- **data-asset** - Information/documentation (CALM specs, ADRs, domain models)

## 🔌 Interface Types

| Interface | Node | Port | Purpose |
|-----------|------|------|---------|
| learning-platform-http | Learning Platform | 8000 | Homepage, API docs, CALM specs |
| task-manager-ui-http | Task Manager UI | 9000 | Interactive UI |
| monolith-api-http | Monolith API | 8001 | REST endpoints |
| monolith-swagger-ui | Monolith API | 8001 | API documentation |
| monolith-db-interface | SQLite Database | N/A | Database connection |

## 🌐 Protocols Used

- **HTTP** - Web browser to services
- **HTTPS** - TLS variant (production)
- **JDBC** - Database connection
- **JSON** - Data format

## 📝 Metadata Fields

```json
{
  "version": "1.0.0",
  "created-by": "Gaurang Karia",
  "created-date": "2025-11-11",
  "purpose": "Educational platform",
  "domain": "Task Management",
  "technologies": ["Python/FastAPI", "SQLite", "Vanilla JS", "Tailwind CSS"],
  "deployment": "Render.com (Free Tier)",
  "environment": "Development"
}
```

## 🎓 Educational Use Cases

This CALM spec can be used for:

1. **Learning** - Understand how components interact
2. **Documentation** - Reference for system architecture
3. **Comparison** - Template for other pattern implementations
4. **Analysis** - Parse JSON for automated architecture analysis
5. **Validation** - Verify compliance with standards

## 🔄 Integration with Project

### Platform App (`platform/app.py`)
- Serves CALM specs via `/calm/{arch_id}` endpoint
- Uses specification to display architecture info

### Monolith API (`sample-app/01-monolith/app.py`)
- Implements interfaces defined in nodes
- Enforces controls (rate limiting, sanitization)

### Task Manager UI (`task-manager-ui/app.js`)
- Follows UI node interface definition
- Connects to monolith-api via HTTP

## 🚀 Extending the Architecture

### Add New Pattern
1. Create new service node (e.g., `microservices-api`)
2. Define relationships from task manager UI
3. Add new flow showing pattern-specific process
4. Document new controls if pattern adds security features

### Add New Flow
```json
{
  "unique-id": "new-flow-id",
  "name": "Flow Name",
  "description": "What this flow demonstrates",
  "transitions": [
    {
      "relationship-unique-id": "existing-relationship-id",
      "sequence-number": 1,
      "description": "Step description"
    }
  ]
}
```

## ✅ Validation Checklist

- [ ] All node unique-ids are unique across architecture
- [ ] All relationship-unique-ids are unique
- [ ] All referenced nodes exist
- [ ] All referenced relationships exist in flows
- [ ] All interface references match defined interfaces
- [ ] Protocol values are from CALM enum
- [ ] No trailing commas in JSON
- [ ] Schema reference is correct (`https://calm.finos.org/release/1.0/meta/calm.json`)

## 📖 CALM Resources

- [FINOS CALM Official Docs](https://calm.finos.org)
- [CALM v1.0 Schema](https://calm.finos.org/release/1.0/meta/calm.json)
- [Calm CLI](https://github.com/finos/calm/wiki/CLI)

---

**Last Updated**: 2025-11-11  
**Validation Status**: ✅ PASSED  
**CALM Version**: 1.0
