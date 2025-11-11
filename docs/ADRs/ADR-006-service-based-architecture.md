# ADR-006: Service-Based Architecture

**Status:** Accepted
**Date:** 2025-11-11

## Decision
Implement **Service-Based Architecture** with coarse-grained services sharing a database.

## Rationale
- **Middle Ground**: Between monolith and microservices
- **Simpler than Microservices**: Fewer services to manage
- **Shared Database**: Easier data consistency
- **Service Independence**: Some deployment independence

## Characteristics
- **Coarse-Grained**: Larger services (not fine-grained microservices)
- **Shared Database**: All services use same database
- **Domain-Driven**: Services organized by business capability

## Trade-offs
**Positive:** Simpler than microservices, some independence, easier data management
**Negative:** Still coupled via database, limited scalability, shared deployment sometimes needed

## When to Use
- Medium-sized applications
- Need some service independence without full microservices complexity
- Database transactions across services needed
- Limited DevOps maturity
