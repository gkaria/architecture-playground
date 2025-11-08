# ADR-001: Start with Monolithic Architecture

**Status:** Accepted

**Date:** 2025-11-08

**Decision Makers:** Architecture Patterns Playground Team

---

## Context

We are building an educational platform to teach software architecture patterns through practical implementations. We need to demonstrate multiple architectural styles using the same domain model (Task Manager application). The question is: which architecture pattern should we implement first?

### Key Considerations

1. **Educational Value**: The implementation should clearly demonstrate architectural concepts
2. **Development Speed**: We want to deliver a working example quickly
3. **Foundation for Comparison**: The first implementation will serve as a baseline for comparing other patterns
4. **Simplicity**: We need to minimize cognitive load for learners who may be new to architecture concepts
5. **Evolution Path**: The architecture should demonstrate a realistic starting point that can evolve

### Alternatives Considered

1. **Monolithic Architecture**
   - Single deployment unit with all features
   - Direct function calls between components
   - Shared database
   - Simple deployment model

2. **Microservices Architecture**
   - Distributed services from day one
   - Independent deployment and scaling
   - Higher complexity but demonstrates modern patterns

3. **Modular Monolith**
   - Single deployment with enforced module boundaries
   - Middle ground between monolith and microservices
   - Better organization but more upfront design

---

## Decision

We will implement the **Monolithic Architecture** as the first pattern in the Architecture Patterns Playground.

### Rationale

1. **Natural Starting Point**: Most real-world systems start as monoliths. This reflects actual software evolution and provides an authentic learning experience.

2. **Lowest Complexity**: A monolith has the fewest moving parts:
   - No distributed system concerns
   - No network communication between components
   - No service discovery or orchestration
   - Single database transaction scope

3. **Fastest Time to Value**: We can deliver a fully working implementation quickly, allowing learners to see a complete system in action before exploring more complex patterns.

4. **Clear Baseline**: The monolith provides a simple reference point for comparison:
   - "This is what we start with"
   - "Here's what changes with each pattern"
   - Clear before/after comparisons

5. **Realistic Evolution Story**: Demonstrates the common architectural journey:
   - Start simple (monolith)
   - Grow and refactor (modular monolith)
   - Scale and distribute (microservices, event-driven)

6. **Teaching Fundamentals**: Forces focus on core concepts:
   - Domain modeling
   - API design
   - Data persistence
   - Error handling
   - Without distraction of distributed systems complexity

---

## Consequences

### Positive

✅ **Rapid Development**: Can build and deploy the first implementation quickly

✅ **Easy to Understand**: Learners can grasp the entire system in one codebase

✅ **Simple Infrastructure**: No container orchestration, service mesh, or message brokers needed initially

✅ **Straightforward Testing**: All code is in one place, making integration testing simple

✅ **Performance**: No network latency between components for baseline performance measurements

✅ **ACID Transactions**: Easy to maintain data consistency with a single database

✅ **Debugging**: Straightforward debugging with standard tools and stack traces

### Negative

❌ **Not Representative of Complex Systems**: Learners may need to understand that real-world large systems often can't stay monolithic

❌ **Scalability Limitations**: Demonstrates a pattern that has known scaling challenges

❌ **Coupling**: May need to explicitly teach about the coupling issues that emerge in monoliths

❌ **Technology Lock-in**: All components must use the same technology stack

### Neutral

⚖️ **Foundation for Migration**: Will need to show how to refactor/evolve this monolith into other patterns

⚖️ **Educational Completeness**: Must be clear this is one of many valid patterns, not "the right way"

---

## Implementation Details

### Technology Stack
- **Framework**: FastAPI (Python) - modern, fast, well-documented
- **Database**: SQLite - zero configuration, easy to demonstrate
- **Caching**: In-memory Python dictionary - simplest possible cache
- **Deployment**: Single container or process

### Architecture Components

```
┌─────────────────────────────────────┐
│   Task Manager Monolith (FastAPI)   │
│                                     │
│  ┌────────────┐  ┌──────────────┐  │
│  │ API Layer  │  │    Cache     │  │
│  └─────┬──────┘  └──────────────┘  │
│        │                            │
│  ┌─────▼──────────────────────┐    │
│  │   Business Logic Layer     │    │
│  └─────┬──────────────────────┘    │
│        │                            │
│  ┌─────▼──────────────────────┐    │
│  │   Data Access Layer        │    │
│  └─────┬──────────────────────┘    │
└────────┼────────────────────────────┘
         │
    ┌────▼────┐
    │ SQLite  │
    └─────────┘
```

### Domain Model
The monolith will implement the complete Task Manager domain:
- Tasks (CRUD operations)
- Users (basic structure)
- Projects (basic structure)

### API Endpoints
- `POST /tasks` - Create task
- `GET /tasks` - List tasks
- `GET /tasks/{id}` - Get task
- `PUT /tasks/{id}` - Update task
- `PATCH /tasks/{id}/status` - Update status
- `DELETE /tasks/{id}` - Delete task

---

## Follow-up Decisions

This decision creates the need for several follow-up decisions:

- **ADR-002**: Choice of database (SQLite vs. PostgreSQL)
- **ADR-003**: Caching strategy
- **ADR-004**: API framework selection (FastAPI)
- **Future ADRs**: Evolution to other architectural patterns

---

## References

- **Fundamentals of Software Architecture** by Mark Richards & Neal Ford
  - Chapter on Monolithic Architecture
  - Discussion of when monoliths are appropriate

- **FINOS CALM Framework**: Used to document this architecture in machine-readable format
  - See: `/calm-specs/monolith/architecture.json`

- **Monolith Implementation**: `/sample-app/01-monolith/`

---

## Review and Update History

- 2025-11-08: Initial decision to implement monolithic architecture first
- Status: Accepted and Implemented
