# CALM Architecture Documentation Index

## 📍 Quick Navigation

| Document | Purpose | Audience |
|----------|---------|----------|
| **SUMMARY.md** | Comprehensive architecture overview | Architects, Developers |
| **REFERENCE.md** | Quick reference and commands | Developers, DevOps |
| **system.architecture.json** | Raw CALM specification (v1.0) | Tools, Automation |
| **../docs/ADRs/ADR-001-*.md** | Architecture Decision Records | All |
| **../README.md** | Project overview | New users |

---

## 🎯 What is This?

The **Architecture Patterns Playground** is an educational platform that demonstrates how the same Task Manager application can be implemented using 6 different architectural patterns. This CALM specification documents the current system (Monolithic phase) in machine-readable format.

---

## 🚀 Getting Started

### 1. View the Architecture
```bash
# Pretty-print the CALM JSON
cat system.architecture.json | python -m json.tool | head -100

# Or open in an editor
code system.architecture.json
```

### 2. Understand the Components
- Read **SUMMARY.md** for a complete overview
- See **REFERENCE.md** for quick reference tables
- Check **../README.md** for project context

### 3. Validate the Specification
```bash
calm validate -a system.architecture.json
```

### 4. Explore the Code
- **../platform/app.py** - Learning platform (Port 8000)
- **../sample-app/01-monolith/app.py** - REST API (Port 8001)
- **../task-manager-ui/app.js** - Frontend (Port 9000)

---

## 📚 CALM Specification Structure

### Nodes (9)
The building blocks of the architecture:
- **2 Actors**: Developer, Web Browser
- **2 Services**: Learning Platform, Monolith API
- **1 Frontend**: Task Manager UI
- **1 Database**: SQLite
- **3 Data Assets**: Shared Models, CALM Specs, ADRs

### Relationships (11)
How components connect and interact:
- **4 Business Interactions**: People and systems interacting
- **7 Technical Connections**: Data flows via HTTP/JDBC

### Flows (3)
Business processes traversing the architecture:
1. **Developer Learning Flow** (7 steps)
2. **Task Creation Flow** (6 steps)
3. **Task Retrieval Flow** (6 steps with caching)

### Controls (5)
Security and reliability requirements:
1. Input Sanitization (XSS prevention)
2. Rate Limiting (per-endpoint limits)
3. CORS Policy (restrictive whitelist)
4. Parameterized Queries (SQL injection prevention)
5. Transaction Rollback (error handling)

---

## 🔍 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  DEVELOPER / LEARNER                                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
         ┌──────────────────────────────┐
         │   WEB BROWSER                │
         └──────┬──────────────┬────────┘
                │              │
      ┌─────────▼──────┐  ┌────▼──────────────┐
      │ LEARNING PLATFORM│  │ TASK MANAGER UI  │
      │ (Port 8000)      │  │ (Port 9000)      │
      └────────┬─────────┘  └────────┬─────────┘
               │                    │
               │                    ▼
               │         ┌──────────────────────┐
               │         │  MONOLITH API        │
               │         │  (Port 8001)         │
               │         │  - 6 CRUD endpoints  │
               │         │  - Rate limiting     │
               │         │  - CORS middleware   │
               │         └──────────┬───────────┘
               │                    │
               │         ┌──────────▼───────────┐
               │         │  SQLITE DATABASE     │
               │         │  (tasks.db)          │
               │         │  - 3 tables          │
               │         │  - Transactions      │
               │         └──────────────────────┘
               │
      ┌────────▼──────────────┐
      │  CALM SPECS & ADRs   │
      │  (Documentation)     │
      └──────────────────────┘
```

---

## 🎓 Learning Path

### For New Developers
1. Start with **../README.md** - Understand project goals
2. Run the system locally - See it working
3. Read **SUMMARY.md** - Understand the architecture
4. Review **REFERENCE.md** - Learn about components
5. Study the code - See implementation details
6. Explore ADRs - Understand decisions

### For Architects
1. Review **system.architecture.json** - Formal specification
2. Analyze relationships and flows - Data architecture
3. Examine controls - Security and reliability
4. Compare with other patterns (coming soon) - Trade-offs
5. Create documentation for new patterns

### For Students
1. Understand the domain - Task Management
2. Learn the patterns - Read architecture explanations
3. Try the interactive UI - See patterns in action
4. Compare performance - Use architecture selector
5. Read ADRs - Learn how to make architectural decisions

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **File Size** | 20 KB |
| **Lines** | 582 |
| **Nodes** | 9 |
| **Relationships** | 11 |
| **Flows** | 3 |
| **Controls** | 5 |
| **Schema Version** | CALM v1.0 |
| **Validation Status** | ✅ PASSED |

---

## 🔗 File Locations

```
architecture-playground/
├── calm-specs/                      ← CALM Documentation (YOU ARE HERE)
│   ├── INDEX.md                     ← Master navigation index
│   ├── SUMMARY.md                   ← Comprehensive overview
│   ├── REFERENCE.md                 ← Quick reference guide
│   ├── system.architecture.json     ← Main CALM spec (v1.0)
│   └── monolith/                    (planned: pattern-specific specs)
├── platform/
│   └── app.py                       (serves CALM via API)
├── sample-app/
│   ├── 01-monolith/
│   │   ├── app.py                   (implements monolith pattern)
│   │   └── database.py
│   └── shared/
│       └── domain/                  (Task, User, Project models)
├── task-manager-ui/
│   ├── app.js                       (connects to API)
│   └── index.html
├── docs/
│   └── ADRs/
│       └── ADR-001-*.md             (architecture decisions)
├── README.md                        (project overview)
└── QUICKSTART.md                    (quick start guide)
```

---

## ✅ Validation Status

✅ **PASSED** - CALM v1.0 compliant
- JSON Schema Validation: 0 errors
- Spectral Schema Validation: 0 errors
- All relationships valid
- All node references correct
- All interfaces defined
- All protocols from enum

To revalidate:
```bash
calm validate -a calm-specs/system.architecture.json
```

---

## 🔄 Next Steps

### Immediate (Phase 2)
- [ ] Create CALM spec for Modular Monolith pattern
- [ ] Update platform app to serve monolith CALM spec
- [ ] Document modular boundaries in architecture

### Short Term (Phase 3)
- [ ] Add CALM specs for Microservices pattern
- [ ] Create pattern comparison flow
- [ ] Document service decomposition

### Medium Term (Phase 4-5)
- [ ] Add CALM specs for Event-Driven, Layered, Service-Based
- [ ] Create comprehensive pattern comparison
- [ ] Generate architecture visualization tools

---

## 📖 Resources

### FINOS CALM
- **Official Site**: https://calm.finos.org
- **v1.0 Schema**: https://calm.finos.org/release/1.0/meta/calm.json

### Architecture Resources
- **Fundamentals of Software Architecture** - Richards & Ford
- **Building Microservices** - Sam Newman
- **Domain-Driven Design** - Eric Evans

### Related Standards
- **ADR Format**: https://adr.github.io/
- **OpenAPI/Swagger**: https://swagger.io/specification/
- **JSON Schema**: https://json-schema.org/

---

## ❓ FAQ

**Q: What is CALM?**
A: CALM (Common Architecture Language Model) is a standardized way to document system architectures in machine-readable format.

**Q: How do I validate changes?**
A: Run `calm validate -a system.architecture.json` after modifications.

**Q: Can I modify the architecture?**
A: Yes! Follow the CALM schema and revalidate. See REFERENCE.md for examples.

**Q: How do I add a new flow?**
A: Add a transition object to the flows array, referencing existing relationships.

**Q: Why multiple documentation formats?**
A: CALM (machine-readable) + ADRs (human-readable) + README (quick reference) = complete documentation.

---

## 📝 Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-11 | 1.0.0 | Gaurang Karia | Initial CALM architecture created |

---

## 📞 Questions?

- **Architecture Questions**: Review ADRs in `../docs/ADRs/`
- **CALM Questions**: Check REFERENCE.md
- **Implementation Questions**: See ../README.md or ../QUICKSTART.md
- **FINOS CALM Support**: https://calm.finos.org

---

**Status**: ✅ Production Ready  
**Last Updated**: 2025-11-11  
**Validation**: ✅ PASSED  
**CALM Version**: 1.0

---

**Ready to learn architectural patterns? Start with README.md!**
