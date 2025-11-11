# Microservices Implementation

This directory contains the **Microservices** implementation of the Task Manager application.

## Architecture Overview

A **Microservices Architecture** decomposes the application into small, independent services that can be developed, deployed, and scaled independently. Each service has its own database and communicates with others via APIs.

### Key Characteristics

- **Independent Services**: Each service runs as a separate process
- **Service-specific Databases**: Each service has its own database (database per service pattern)
- **API Gateway**: Single entry point for clients, routes requests to services
- **Independent Deployment**: Services can be deployed independently
- **Independent Scaling**: Services can be scaled based on individual needs
- **Polyglot Persistence**: Services can use different database technologies

## Directory Structure

```
03-microservices/
├── api-gateway/                # API Gateway
│   └── app.py                 # Routes requests to services
├── task-service/              # Task management service
│   └── app.py                 # Task CRUD operations
├── user-service/              # User management service (placeholder)
│   └── app.py                 # User operations
├── project-service/           # Project management service (placeholder)
│   └── app.py                 # Project operations
├── docker-compose.yml         # Orchestrate all services
└── README.md
```

## Services

### 1. API Gateway (Port 8006)
- **Purpose**: Single entry point for all client requests
- **Responsibilities**:
  - Route requests to appropriate microservices
  - Handle service discovery
  - Aggregate responses (if needed)
  - Provide unified error handling

### 2. Task Service (Port 8003)
- **Purpose**: Manage tasks
- **Database**: `task_service.db` (SQLite)
- **Endpoints**: Full CRUD for tasks
- **Independent**: Can be deployed and scaled independently

### 3. User Service (Port 8004) - Placeholder
- **Purpose**: Manage users
- **Status**: Planned for future implementation

### 4. Project Service (Port 8005) - Placeholder
- **Purpose**: Manage projects
- **Status**: Planned for future implementation

## Running the Services

### Option 1: Run Task Service + Gateway Manually

Start Task Service:
```bash
cd task-service
PORT=8003 python app.py
```

Start API Gateway (in another terminal):
```bash
cd api-gateway
PORT=8006 python app.py
```

### Option 2: Use Docker Compose (Recommended)
```bash
cd sample-app/03-microservices
docker-compose up
```

The API Gateway will be available at `http://localhost:8006`

## API Endpoints

All requests go through the API Gateway:

- `GET /` - Gateway information
- `GET /health` - Health check (gateway + services)
- `POST /tasks` - Create a task (routed to task-service)
- `GET /tasks` - List all tasks (routed to task-service)
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `PATCH /tasks/{id}/status` - Update task status
- `DELETE /tasks/{id}` - Delete a task

## Service Communication

```
Client → API Gateway → Task Service → Task Database
                    → User Service → User Database
                    → Project Service → Project Database
```

## Comparison with Previous Patterns

| Aspect | Monolith | Modular Monolith | Microservices |
|--------|----------|------------------|---------------|
| **Deployment** | Single unit | Single unit | Multiple units |
| **Database** | Shared | Shared | Per service |
| **Scaling** | All together | All together | Independent |
| **Complexity** | Low | Medium | High |
| **Team Independence** | Low | Medium | High |
| **Deployment Risk** | High | High | Low (per service) |
| **Network Calls** | None | None | Yes (overhead) |
| **Data Consistency** | Easy (ACID) | Easy (ACID) | Hard (eventual) |

## Advantages

1. **Independent Deployment**: Deploy services without affecting others
2. **Independent Scaling**: Scale services based on individual load
3. **Technology Flexibility**: Each service can use different tech stack
4. **Team Autonomy**: Teams can own and evolve services independently
5. **Fault Isolation**: Failure in one service doesn't crash entire system
6. **Parallel Development**: Multiple teams can work simultaneously

## Disadvantages

1. **Increased Complexity**:
   - Network latency between services
   - Distributed system challenges
   - More infrastructure to manage

2. **Data Consistency Challenges**:
   - No distributed transactions
   - Eventual consistency model
   - Complex queries across services

3. **Testing Complexity**:
   - Integration testing is harder
   - Need to mock service dependencies
   - End-to-end tests are complex

4. **Operational Overhead**:
   - More deployment pipelines
   - More monitoring and logging
   - Service discovery and load balancing

5. **Network Overhead**:
   - HTTP calls between services
   - Serialization/deserialization cost
   - Potential performance impact

## When to Use

- **Large teams** that need to work independently
- **Services with different scaling needs**
- **Organizations** practicing DevOps and continuous deployment
- **Systems** requiring high availability and fault tolerance
- **Applications** where different parts use different technologies

## When NOT to Use

- **Small applications** - overhead outweighs benefits
- **Tight coupling** - if services need to change together frequently
- **Simple CRUD** - monolith or modular monolith is simpler
- **Limited DevOps maturity** - requires strong infrastructure

## Design Patterns

### 1. Database per Service
Each service owns its database. No direct database access between services.

### 2. API Gateway Pattern
Single entry point for clients, hiding service complexity.

### 3. Service Discovery
Services register themselves and discover others (simplified in this implementation).

### 4. Circuit Breaker
Prevent cascading failures (not implemented in basic version).

## Security Features

- **Rate Limiting**: Applied at service level
- **Input Sanitization**: Each service validates inputs
- **CORS**: Configured for cross-origin requests
- **Service Authentication**: (Not implemented - would use JWT/OAuth in production)

## Data Management Challenges

### Challenge 1: Joins Across Services
- **Problem**: Cannot JOIN data across service databases
- **Solution**: Use API composition or CQRS pattern

### Challenge 2: Transactions Across Services
- **Problem**: No distributed ACID transactions
- **Solution**: Use Saga pattern or eventual consistency

### Challenge 3: Data Duplication
- **Problem**: Same data might exist in multiple services
- **Solution**: Each service owns its bounded context

## Monitoring and Observability

In production, you would add:
- **Distributed Tracing**: Track requests across services (Jaeger, Zipkin)
- **Centralized Logging**: Aggregate logs (ELK Stack, Splunk)
- **Metrics Collection**: Monitor service health (Prometheus, Grafana)
- **Service Mesh**: Handle service communication (Istio, Linkerd)

## Migration from Modular Monolith

This architecture evolved from the modular monolith (Phase 2):

1. **Modules → Services**: Each module became an independent service
2. **Shared Database → Per-Service**: Split database by service boundaries
3. **Function Calls → HTTP**: Module communication became API calls
4. **Single Deploy → Multiple**: Each service deploys independently

## Testing Strategy

1. **Unit Tests**: Test service logic in isolation
2. **Integration Tests**: Test service with its database
3. **Contract Tests**: Test service API contracts
4. **End-to-End Tests**: Test entire flow through gateway
5. **Consumer-Driven Contract Tests**: Services agree on API contracts

## Deployment Considerations

### Development
- Run all services locally
- Use docker-compose for orchestration

### Production
- **Container Orchestration**: Kubernetes, Docker Swarm
- **Service Registry**: Consul, Eureka
- **Load Balancer**: NGINX, HAProxy
- **API Gateway**: Kong, Tyk, AWS API Gateway
- **Message Queue**: RabbitMQ, Kafka (for async communication)

## Educational Value

This pattern teaches:

1. **Service Decomposition**: Breaking monolith into services
2. **Distributed Systems**: Handling network calls and failures
3. **API Design**: Designing service interfaces
4. **Data Ownership**: Database per service pattern
5. **Service Orchestration**: Managing multiple services

## Common Pitfalls

1. **Too Many Services**: Start with fewer services, split when needed
2. **Chatty Services**: Minimize inter-service calls
3. **Distributed Monolith**: Services that must deploy together
4. **Ignoring Network Failures**: Always handle timeouts and retries
5. **Shared Database**: Defeats the purpose of microservices

## Future Enhancements

- Implement user and project services
- Add service-to-service authentication
- Implement circuit breaker pattern
- Add distributed tracing
- Implement API rate limiting at gateway
- Add caching layer (Redis)
- Implement event-driven communication between services

## References

- **Martin Fowler**: "Microservices" - https://martinfowler.com/articles/microservices.html
- **Chris Richardson**: "Microservices Patterns" - https://microservices.io/
- **Sam Newman**: "Building Microservices" book
- **CALM Specification**: `calm-specs/microservices.architecture.json`
- **ADR-003**: Architecture Decision Record
