# CALM Architecture for Architecture Patterns Playground

## ✅ Validation Status

**Status**: **PASSED** ✓
- JSON Schema Validation: ✅ 0 errors
- Spectral Schema Validation: ✅ 0 errors  
- CALM v1.0 Compliance: ✅ Verified

**Validation Command**:
```bash
calm validate -a system.architecture.json
```

## 📋 Architecture Overview

**File**: `system.architecture.json`
**Location**: `calm-specs/system.architecture.json`
**Size**: 20 KB | **Lines**: 582

This CALM specification documents the **Architecture Patterns Playground** - an educational platform demonstrating how the same Task Manager application can be implemented using 6 different architectural patterns.

## 🏗️ Architecture Components

### Actors (2)
- **developer** - Software developer/learner exploring the playground
- **browser** - Client device running web browser

### Services (2)
- **learning-platform** (Port 8000) - FastAPI educational platform with Jinja2 templates
- **monolith-api** (Port 8001) - FastAPI REST API with 6 CRUD endpoints

### Frontend (1)
- **task-manager-ui** (Port 9000) - Vanilla JavaScript UI with architecture selector

### Data Storage (1)
- **monolith-database** - SQLite database (tasks.db) with 3 tables

### Data Assets (3)
- **shared-domain-models** - Reusable Task, User, Project entities
- **calm-specifications** - CALM docs for all 6 architectural patterns
- **architecture-decision-records** - ADRs explaining architectural choices

## 🔗 Relationships (11)

**Business Interactions** (4):
- developer → browser
- learning-platform → task-manager-ui
- monolith-api → shared-domain-models
- calm-specifications → shared-domain-models

**Technical Connections** (7):
- browser → learning-platform (HTTP)
- browser → task-manager-ui (HTTP)
- task-manager-ui → monolith-api (HTTP)
- learning-platform → monolith-api (HTTP)
- monolith-api → monolith-database (JDBC)
- learning-platform → calm-specifications (JSON)
- learning-platform → architecture-decision-records

## 📊 Flows (3)

### 1. **Developer Learning Flow**
7-step journey showing how a developer explores:
- Views homepage → Pattern overview
- Reads CALM specs → Design documentation
- Reviews ADRs → Architectural decisions
- Tries interactive UI → Hands-on experience
- Connects to monolith API → Testing

### 2. **Task Creation Flow**
6-step task creation process:
- Form submission → Validation
- Domain model creation → Sanitization
- Database insertion → Cache invalidation
- Response returned → UI update

### 3. **Task Retrieval Flow** (with Caching)
6-step cached retrieval process:
- Request from UI → In-memory cache check
- Cache hit/miss → Database query or return cached data
- Populate cache → 60-second TTL
- Return task list → Render in UI

## 🔒 Controls (5)

All security controls documented:

1. **Input Sanitization** - XSS prevention using bleach library
2. **Rate Limiting** - 100/min reads, 30/min writes, 20/min creates
3. **CORS Policy** - Restrictive whitelist (no wildcards)
4. **Parameterized Queries** - SQL injection prevention
5. **Transaction Rollback** - Automatic error handling

## 📐 Key Metadata

- **Purpose**: Educational - Learn architectural patterns through implementations
- **Domain**: Task Management
- **Technologies**: Python/FastAPI, SQLite, Vanilla JS, Tailwind CSS, FINOS CALM
- **Deployment**: Render.com (Free Tier)
- **Environment**: Development
- **Version**: 1.0.0

## 🎯 Educational Value

This CALM specification serves as:

1. **Machine-Readable Documentation** - Developers can parse and analyze the architecture programmatically
2. **Standardized Format** - Uses FINOS CALM v1.0 schema for industry-standard compliance
3. **Comparison Basis** - Template for documenting the other 5 architectural patterns
4. **Learning Tool** - Shows how different patterns can implement the same domain

## 📚 Related Documentation

- **CALM Specifications**: This directory (calm-specs/)
- **Architecture Decision Records**: `../docs/ADRs/`
- **Project README**: `../README.md`
- **Quick Start Guide**: `../QUICKSTART.md`

## 🔄 Integration Points

### Platform App
- Reads CALM specs via `/calm/{arch_id}` endpoint
- Displays CALM documentation to learners
- References shared domain models

### Monolith API
- Uses shared domain models for validation
- Provides REST endpoints for CRUD operations
- Enforces security controls (rate limiting, input sanitization)

### Task Manager UI
- Fetches tasks via monolith API
- Uses architecture selector to switch backends
- Displays performance metrics

## 🚀 Next Steps

To extend this architecture:

1. **Add Modular Monolith Pattern** - Create `02-modular-monolith/` implementation
2. **Create Pattern CALM Specs** - Document each new architecture in CALM format
3. **Update Flows** - Document pattern-specific workflows
4. **Record ADRs** - Explain design decisions for each pattern

## 💡 CALM Best Practices Applied

✅ Descriptive node names and descriptions  
✅ Unique IDs using kebab-case  
✅ Comprehensive metadata for operational context  
✅ Business-level flows with clear transitions  
✅ Security controls explicitly documented  
✅ Relationship protocols clearly specified  
✅ Strict CALM v1.0 schema compliance  

---

**Created**: 2025-11-11  
**Status**: Production Ready  
**Validation**: ✅ PASSED
