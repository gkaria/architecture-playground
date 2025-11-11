# ADR-002: Evolve to Modular Monolith Architecture

**Status:** Accepted

**Date:** 2025-11-11

**Decision Makers:** Architecture Patterns Playground Team

**Supersedes:** None (complements ADR-001)

---

## Context

Following the implementation of the monolithic architecture (ADR-001), we need to demonstrate the next evolution step in architectural patterns. As systems grow, monoliths often face challenges with code organization, team scalability, and maintainability. The question is: how do we organize a growing codebase while maintaining deployment simplicity?

### Key Considerations

1. **Code Organization**: As the monolith grows, better code structure is needed
2. **Team Scalability**: Multiple developers need to work on different features without conflicts
3. **Maintainability**: Clear boundaries make the codebase easier to understand and modify
4. **Testing**: Ability to test different parts of the system independently
5. **Migration Path**: Potential for future extraction to microservices if needed
6. **Deployment Simplicity**: Maintain the simple deployment model of a monolith

### Problems with Pure Monolith

From ADR-001 implementation, we've identified these growth challenges:
- All code in single files makes navigation difficult
- No clear boundaries between different concerns
- Testing requires loading entire application
- Difficult for teams to work independently
- Refactoring becomes risky without clear module boundaries

### Alternatives Considered

1. **Modular Monolith**
   - Single deployment unit
   - Code organized into well-defined modules
   - Each module has clear boundaries and responsibilities
   - Modules communicate through defined interfaces

2. **Jump to Microservices**
   - Distributed services with independent deployment
   - Higher complexity, network overhead
   - Overkill for medium-sized applications

3. **Layered Architecture**
   - Horizontal layers (presentation, business, data)
   - Doesn't provide vertical module boundaries
   - Can be combined with modular approach

---

## Decision

We will implement a **Modular Monolith Architecture** where the application remains a single deployment unit, but code is organized into self-contained modules with clear boundaries.

### Architecture Structure

```
app.py (orchestrator)
├── infrastructure/          # Shared infrastructure
│   ├── database.py         # Database connection, base repository
│   └── security.py         # Security utilities
└── modules/                # Business modules
    ├── tasks/              # Task management module
    │   ├── repository.py   # Data access layer
    │   ├── service.py      # Business logic layer
    │   └── router.py       # API routing layer
    ├── users/              # User management module
    └── projects/           # Project management module
```

### Rationale

1. **Maintains Deployment Simplicity**: Still a single process, single database
   - No distributed system complexity
   - Simple deployment process (same as monolith)
   - No network latency between modules

2. **Improves Code Organization**: Clear module boundaries
   - Each module is self-contained
   - Easy to locate code for specific features
   - Reduced cognitive load when working on a feature

3. **Enables Team Scalability**: Teams can own modules
   - Multiple developers can work on different modules simultaneously
   - Reduced merge conflicts
   - Clear ownership boundaries

4. **Better Testability**: Modules can be tested independently
   - Unit test individual layers (repository, service, router)
   - Mock dependencies at module boundaries
   - Integration tests for cross-module interactions

5. **Migration Path**: Provides evolution options
   - Can extract modules to microservices later if needed
   - Module boundaries become service boundaries
   - Low-risk refactoring within module boundaries

6. **Layered Module Architecture**: Each module has consistent layers
   - **Repository**: Data access, database operations
   - **Service**: Business logic, validation, orchestration
   - **Router**: HTTP handling, request/response
   - Clear separation of concerns within each module

---

## Consequences

### Positive

1. **Better Organization**
   - Clear module structure
   - Easy code navigation
   - Reduced cognitive complexity

2. **Independent Development**
   - Teams can work on modules independently
   - Fewer merge conflicts
   - Parallel feature development

3. **Testing Benefits**
   - Test modules in isolation
   - Mock module boundaries
   - Faster test execution

4. **Refactoring Safety**
   - Changes within module boundaries are safe
   - Clear interfaces reduce ripple effects
   - Easier to understand impact of changes

5. **Deployment Simplicity Maintained**
   - Still single deployment unit
   - No distributed system complexity
   - Simple rollback strategy

### Negative

1. **Architectural Discipline Required**
   - Developers must respect module boundaries
   - Temptation to bypass interfaces
   - Requires code reviews to enforce boundaries

2. **Increased File Count**
   - More files to navigate than pure monolith
   - Potential for over-modularization
   - Need for good naming conventions

3. **Not True Service Independence**
   - All modules share same database
   - Cannot scale modules independently
   - Cannot deploy modules independently

4. **Module Communication Overhead**
   - Going through interfaces adds indirection
   - Slightly more complex than direct function calls
   - Need to design module APIs carefully

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Module boundaries violated | Code reviews, architectural tests |
| Over-modularization | Start with few modules, split as needed |
| Shared database bottleneck | Keep in mind for future microservices split |
| Module coupling | Enforce interface-only communication |

---

## Implementation Details

### Module Design Principles

1. **High Cohesion**: Related functionality grouped in same module
2. **Low Coupling**: Modules communicate through defined interfaces only
3. **Layered Within Modules**: Repository → Service → Router
4. **Shared Infrastructure**: Database, security utilities centralized
5. **Domain-Driven**: Modules organized around business capabilities

### Module Communication Rules

- ✅ **Allowed**: Module calls its own layers (router → service → repository)
- ✅ **Allowed**: Module uses shared infrastructure (database, security)
- ✅ **Allowed**: Module imports shared domain models
- ❌ **Forbidden**: Direct access to another module's repository
- ❌ **Forbidden**: Direct access to another module's service
- ⚠️ **Caution**: Cross-module service calls (design carefully)

### Testing Strategy

1. **Unit Tests**: Test individual layers in isolation
2. **Integration Tests**: Test module as a whole
3. **Contract Tests**: Test module API contracts
4. **End-to-End Tests**: Test complete flows across modules

---

## Comparison with Monolith (ADR-001)

| Aspect | Monolith | Modular Monolith |
|--------|----------|------------------|
| **Files** | 3 files | ~10 files |
| **Lines of Code** | ~650 | ~900 (more structure) |
| **Deployment** | Single unit | Single unit |
| **Code Navigation** | Linear search | Module-based navigation |
| **Testing** | Test whole app | Test modules independently |
| **Team Scalability** | Limited | Better |
| **Refactoring Risk** | High | Lower (within modules) |
| **Complexity** | Low | Medium |

---

## Educational Value

This pattern teaches:

1. **Module Boundaries**: How to define and maintain clear boundaries
2. **Layered Architecture**: Repository, service, router separation
3. **Interface Design**: Communication through well-defined interfaces
4. **Refactoring Path**: How monoliths can evolve without full rewrite
5. **Trade-offs**: Balance between simplicity and organization

---

## References

- **ADR-001**: Monolithic Architecture baseline
- **Martin Fowler**: "MonolithFirst" - https://martinfowler.com/bliki/MonolithFirst.html
- **Simon Brown**: "Modular Monoliths" - https://www.youtube.com/watch?v=5OjqD-ow8GE
- **CALM Specification**: `calm-specs/modular-monolith.architecture.json`
- **Implementation**: `sample-app/02-modular-monolith/`

---

## Review and Updates

This ADR should be reviewed when:
- Module boundaries become unclear or violated
- Need to add new modules
- Considering extraction to microservices
- Performance issues arise from module indirection
