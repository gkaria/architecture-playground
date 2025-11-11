# ADR-003: Decompose into Microservices Architecture

**Status:** Accepted
**Date:** 2025-11-11
**Supersedes:** Extends ADR-002

## Context
After implementing modular monolith (ADR-002), we demonstrate the next evolution: independent services that can be deployed and scaled separately. This shows when and how to break apart a monolith into microservices.

## Decision
Implement **Microservices Architecture** with:
- API Gateway (port 8006) - single entry point
- Task Service (port 8003) - independent service with own database
- Database per service pattern
- HTTP-based communication

## Rationale
1. **Independent Deployment**: Services deploy without affecting others
2. **Independent Scaling**: Scale services based on load
3. **Team Autonomy**: Teams own entire service lifecycle
4. **Technology Flexibility**: Each service can use different stack
5. **Fault Isolation**: Service failures don't crash entire system

## Consequences

**Positive:**
- True service independence
- Better scalability and fault tolerance
- Team autonomy

**Negative:**
- Increased operational complexity
- Network latency between services
- Distributed data management challenges
- More difficult testing and debugging

## Comparison

| Aspect | Modular Monolith | Microservices |
|--------|------------------|---------------|
| Deployment | Single | Multiple |
| Database | Shared | Per service |
| Network calls | None | Yes |
| Complexity | Medium | High |

## When to Use
- Large teams needing autonomy
- Services with different scaling needs
- Strong DevOps culture
- High availability requirements

## When NOT to Use
- Small applications
- Limited operational maturity
- Tight coupling between features

## References
- Implementation: `sample-app/03-microservices/`
- CALM: `calm-specs/microservices.architecture.json`
