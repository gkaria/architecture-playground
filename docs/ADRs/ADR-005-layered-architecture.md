# ADR-005: Layered Architecture

**Status:** Accepted
**Date:** 2025-11-11

## Decision
Implement traditional **Layered Architecture** with presentation, business, and data layers.

## Rationale
- **Separation of Concerns**: Clear layer responsibilities
- **Well-Understood**: Traditional, widely-known pattern
- **Easy Testing**: Test layers independently
- **Clear Structure**: Horizontal organization

## Layers
1. **Presentation**: HTTP/API handling
2. **Business**: Business logic and validation
3. **Data**: Database access

## Trade-offs
**Positive:** Clear structure, easy to understand, good separation
**Negative:** Can become monolithic, performance overhead from layers

## When to Use
- Enterprise applications
- Teams familiar with traditional architecture
- Clear separation of technical concerns needed
