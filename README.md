# Architecture Patterns Playground

**Learn Software Architecture by Building**

A portfolio and learning platform that teaches software architecture patterns through practical implementations of a Task Manager application built in 6 different architectural styles.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Live Demo

**Try it now - no installation required!**

- **🌐 Learning Platform**: [https://architecture-playground.onrender.com](https://architecture-playground.onrender.com)
- **✓ Task Manager UI**: [https://architecture-playground-ui.onrender.com](https://architecture-playground-ui.onrender.com)
- **🔧 Monolith API Docs**: [https://architecture-playground-api.onrender.com/docs](https://architecture-playground-api.onrender.com/docs)

> **Note**: Free tier services may take 30-60 seconds to wake up on first visit.

---

## What is This?

This project demonstrates how the **same application domain** (a Task Manager) can be implemented using different architectural patterns. Each implementation is:

- ✅ **Fully working code** you can run and modify
- ✅ **Interactive UI** that connects to different backend architectures
- ✅ **Documented with CALM specs** (FINOS Common Architecture Language Model)
- ✅ **Explained with ADRs** (Architecture Decision Records)
- ✅ **Compared side-by-side** to understand trade-offs

### 🎯 NEW: Interactive Task Manager UI

Experience architecture patterns hands-on with a **common frontend** that connects to different backend implementations:

- **Same UI, Different Backend** - Switch between architectures with a dropdown
- **Performance Comparison** - See real-time response times
- **Live Statistics** - Monitor task metrics across architectures
- **Educational** - Learn how architecture is transparent to users

Visit: **http://localhost:9000** (after starting the Task Manager UI server)

### The Goal

Help developers understand:
- When to use each architectural pattern
- The trade-offs and consequences of architectural decisions
- How to document and communicate architecture
- How systems evolve from simple to complex

---

## Architecture Patterns (6 Implementations)

### ✅ Phase 1 - Implemented

1. **Monolithic Architecture** (`sample-app/01-monolith/`)
   - Single deployment unit with shared database
   - Simple, fast to develop, easy to deploy
   - **Status**: ✅ LIVE
   - **Port**: 8001

### 🚧 Coming Soon

2. **Modular Monolith** (`sample-app/02-modular-monolith/`)
   - Clear module boundaries within a single deployment
   - Better organization while maintaining monolith benefits

3. **Microservices Architecture** (`sample-app/03-microservices/`)
   - Independent services with separate databases
   - Maximum scalability and team autonomy

4. **Event-Driven Architecture** (`sample-app/04-event-driven/`)
   - Asynchronous communication through events
   - High scalability and loose coupling

5. **Layered Architecture** (`sample-app/05-layered/`)
   - Traditional horizontal layers (presentation, business, data)
   - Well-understood enterprise pattern

6. **Service-Based Architecture** (`sample-app/06-service-based/`)
   - Coarse-grained services with shared database
   - Practical middle ground between monolith and microservices

---

## Project Structure

```
architecture-playground/
├── platform/                    # Learning platform website
│   ├── app.py                  # FastAPI app
│   ├── templates/              # HTML templates with Tailwind
│   │   ├── home.html
│   │   ├── architecture_detail.html
│   │   └── comparison.html
│   └── static/
│
├── task-manager-ui/            # 🎯 NEW: Interactive Task Manager UI
│   ├── index.html              # Main UI
│   ├── app.js                  # JavaScript application
│   ├── server.py               # Web server (Port 9000)
│   └── README.md               # UI documentation
│
├── sample-app/                 # Task Manager implementations
│   ├── shared/
│   │   └── domain/            # Shared domain models
│   │       ├── task.py        # Task entity
│   │       ├── user.py        # User entity
│   │       └── project.py     # Project entity
│   │
│   ├── 01-monolith/           # Monolithic implementation
│   │   ├── app.py             # FastAPI application
│   │   ├── database.py        # SQLite database layer
│   │   └── README.md          # Pattern explanation
│   │
│   ├── 02-modular-monolith/   # Coming soon...
│   ├── 03-microservices/      # Coming soon...
│   ├── 04-event-driven/       # Coming soon...
│   ├── 05-layered/            # Coming soon...
│   └── 06-service-based/      # Coming soon...
│
├── calm-specs/                # CALM documentation (JSON)
│   ├── monolith/
│   │   └── architecture.json  # CALM spec for monolith
│   └── comparisons/
│
├── docs/
│   ├── ADRs/                  # Architecture Decision Records
│   │   └── ADR-001-monolithic-architecture.md
│   └── learning-notes/
│
└── README.md                  # This file
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Learning Platform

```bash
cd platform
python app.py
```

Visit http://localhost:8000 to explore the learning platform.

### 3. Run the Monolith Implementation

```bash
cd sample-app/01-monolith
python app.py
```

Visit http://localhost:8001/docs for the API documentation.

### 4. Run the Interactive Task Manager UI (🎯 NEW!)

In a new terminal:

```bash
cd task-manager-ui
python server.py
```

Visit http://localhost:9000 to use the Task Manager UI.

**Features:**
- Create, update, and delete tasks
- Switch between different backend architectures
- See real-time performance metrics
- Filter tasks by status

---

## Security Notice

This project implements **basic security features** suitable for portfolio and learning purposes:

### ✅ Implemented Security Features
- **Rate Limiting**: Prevents API abuse with different limits for read/write operations
  - Read operations: 100 requests/minute
  - Write operations: 30 requests/minute
  - Create operations: 20 requests/minute
- **Input Sanitization**: Prevents XSS attacks by sanitizing user inputs
- **CORS Configuration**: Restrictive origin whitelisting (not wildcards)
- **Request Size Limits**: Enforced via Pydantic validation (title: 200 chars, description: 2000 chars)

### ⚠️ Not Suitable for Production

**This is an educational project. For production use, you would need:**

- **Authentication & Authorization**: User login, JWT tokens, role-based access control
- **HTTPS/TLS Encryption**: All communications should be encrypted
- **Database Security**:
  - Switch from SQLite to PostgreSQL
  - Use connection pooling
  - Implement prepared statements (already done via ORM)
  - Enable encryption at rest
- **Advanced Rate Limiting**: Token bucket algorithm, per-user limits, DDoS protection
- **Security Headers**: CSP, X-Frame-Options, HSTS, etc.
- **Input Validation**: Schema validation beyond basic sanitization
- **Logging & Monitoring**: Security event logging, intrusion detection
- **API Gateway**: Centralized security, authentication, and rate limiting
- **Secrets Management**: Vault for API keys, database credentials
- **Vulnerability Scanning**: Regular dependency audits, penetration testing

### 🔒 Security Best Practices

For learning purposes, this project demonstrates:
- How to integrate security libraries (slowapi, bleach)
- Basic input sanitization patterns
- CORS configuration for multi-origin support
- Rate limiting implementation

**Remember**: Never deploy educational code directly to production without a proper security audit and hardening.

---

## Domain Model

All implementations use the same Task Manager domain:

### Entities

**Task**
- id, title, description
- status (todo/in_progress/done)
- priority (low/medium/high)
- user_id, project_id
- created_at, updated_at, due_date
- tags (list)

**User**
- id, username, email, full_name

**Project**
- id, name, description
- owner_id, members (list)

---

## Technology Stack

### Backend
- **Python 3.11+** - Modern Python with type hints
- **FastAPI** - High-performance async web framework
- **SQLite** - Embedded database (upgradable to PostgreSQL/Firestore)
- **Pydantic** - Data validation and settings

### Frontend (Platform)
- **FastAPI Templates** - Server-side rendering
- **Tailwind CSS** - Utility-first CSS (via CDN)
- **No JavaScript frameworks** - Keep it simple

### Documentation
- **FINOS CALM** - JSON-based architecture specifications
- **ADRs** - Markdown-based decision records

### Hosting
- **Render.com** - Free tier deployment ready

---

## Documentation Approach

### CALM Specifications (JSON)

Each architecture is documented using [FINOS CALM](https://calm.finos.org) - the Common Architecture Language Model. This provides:

- **Machine-readable** architecture documentation
- **Standardized** format for comparison
- **Industry-standard** approach

Example: `calm-specs/monolith/architecture.json`

### Architecture Decision Records (ADRs)

Key decisions are documented as ADRs in `docs/ADRs/`:

- **ADR-001**: Why we started with monolithic architecture
- **Future ADRs**: Technology choices, pattern transitions

Format:
- **Status**: Accepted/Proposed/Deprecated
- **Context**: Why we need to decide
- **Decision**: What we decided
- **Consequences**: Positive and negative outcomes

---

## Learning Path

### Recommended Order

1. **Start with Monolith** - Understand the baseline
2. **Study the CALM spec** - Learn architecture documentation
3. **Read ADR-001** - Understand the decision-making process
4. **Explore the platform** - Compare patterns side-by-side
5. **Modular Monolith** - See how to add structure
6. **Microservices** - Understand distribution complexity
7. **Event-Driven** - Learn asynchronous patterns

### Key Concepts Covered

- **Architecture Patterns**: Monolith, Modular Monolith, Microservices, Event-Driven, Layered, Service-Based
- **Trade-off Analysis**: Complexity vs. Scalability, Coupling vs. Performance
- **Documentation**: CALM specs, ADRs, architectural diagrams
- **Evolution**: How architectures change over time
- **Quality Attributes**: Scalability, Availability, Maintainability, Performance

---

## Deployment

### Local Development

```bash
# Run platform
cd platform && python app.py

# Run monolith
cd sample-app/01-monolith && python app.py
```

### Render.com Deployment

Each implementation includes a `render.yaml` for easy deployment:

```bash
# Deploy to Render.com (free tier)
render deploy
```

---

## Roadmap

### Phase 1 - MVP (✅ Complete)
- [x] Monolith implementation
- [x] Platform homepage
- [x] Shared domain models
- [x] First CALM spec
- [x] First ADR

### Phase 2 - Modular Monolith
- [ ] Module boundaries
- [ ] Internal interfaces
- [ ] CALM spec
- [ ] Migration ADR

### Phase 3 - Microservices
- [ ] Service decomposition
- [ ] API gateway
- [ ] Service discovery
- [ ] CALM spec

### Phase 4 - Event-Driven
- [ ] Message broker
- [ ] Event handlers
- [ ] Async processing
- [ ] CALM spec

### Phase 5 - Layered & Service-Based
- [ ] Layered implementation
- [ ] Service-based implementation
- [ ] Final comparisons
- [ ] Complete documentation

---

## Contributing

This is a learning project, but contributions are welcome!

### Areas for Improvement
- Additional architecture patterns
- Better visualizations
- More detailed comparisons
- Test coverage
- Deployment guides

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Inspiration and References

### Books
- **Fundamentals of Software Architecture** by Mark Richards & Neal Ford
- **Building Microservices** by Sam Newman
- **Domain-Driven Design** by Eric Evans

### Standards
- [FINOS CALM](https://calm.finos.org) - Common Architecture Language Model
- [ADR Documentation](https://adr.github.io/) - Architecture Decision Records

### Concepts
- Domain-Driven Design principles
- Evolutionary Architecture
- Trade-off Analysis

---

## License

MIT License - See LICENSE file for details

---

## Author

**Architecture Patterns Playground**

Built as a learning and portfolio project to:
- Demonstrate architectural thinking
- Practice documentation
- Build a useful teaching tool
- Learn by building real implementations

---

## Questions?

- Check the `/docs` folder for detailed documentation
- Review CALM specs in `/calm-specs`
- Read ADRs in `/docs/ADRs`
- Explore the code in `/sample-app`

**Learn by building. Understand by comparing.**
