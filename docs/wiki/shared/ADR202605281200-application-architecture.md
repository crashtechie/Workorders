# ADR-001: Application Architecture

**Date:** 2026-05-28  
**Status:** Accepted  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** The Workorders MVP must serve multiple user roles across multiple device types while maintaining clear ownership of business logic, data, and presentation concerns.
- **Driving factors:** Need for independent deployability, clear API contracts between frontend and backend, and the ability to iterate on each layer without coupling risk.
- **Deadline:** Must be established before any implementation begins to prevent re-architecture mid-project.
- **Affected components:** All services — frontend, backend, database, and deployment infrastructure.

---

## Considered Options

### Option 1: Layered Web Architecture (Separate Frontend and Backend Services)

**Description:** A dedicated Django backend service exposes a REST API via Django REST Framework; a dedicated React/Nginx frontend application consumes it. Each is independently deployed via Docker containers.

**Pros:**
- Clear separation of concerns between UI and business logic
- Independent deployment and scaling of frontend and backend
- Enables explicit API versioning and contract testing
- Allows frontend to be replaced or supplemented (mobile client, CLI) without rewriting business logic

**Cons:**
- Requires discipline in maintaining API contracts
- Network boundary adds latency overhead vs. monolithic server-rendered approach
- Two deployment artifacts to manage instead of one

### Option 2: Monolithic Server-Rendered Application

**Description:** A single application renders HTML on the server and embeds business logic in the same codebase.

**Pros:**
- Simpler initial deployment
- No cross-origin or API versioning concerns

**Cons:**
- Tightly couples presentation and business logic, complicating future evolution
- Harder to support mobile or alternative clients
- Scaling frontend and backend independently is not possible

### Option 3: Serverless Functions with Static Frontend

**Description:** Individual serverless functions handle business logic; a static site handles UI.

**Pros:**
- Low infrastructure overhead
- Scales per function on demand

**Cons:**
- Cold-start latency is undesirable for interactive workorder workflows
- Harder to maintain transactional consistency across functions
- Vendor lock-in risk for a business-critical internal tool

---

## Decision Outcome

> **Decided:** We will use a **layered web architecture** with a separate Django (with Django REST Framework) backend service and a React/Nginx frontend service, each deployed as Docker containers and communicating via a versioned REST API.

---

## Rationale

1. **Best fit for requirements:** The role-based, data-intensive workorder domain benefits from a backend that owns all validation, authorization, and persistence.
2. **Long-term scalability:** Independent containers allow each layer to scale and evolve without redeployment of the other.
3. **Team expertise:** Django/DRF (Python) and React are the chosen stack; Django's batteries-included approach aligns with the team's delivery goals. See ADR-008 for backend framework selection rationale.
4. **Maintenance & support:** Both technologies are actively maintained with large communities.
5. **Integration:** Explicit REST API contracts enable future mobile clients or third-party integrations at defined extension points.
6. **Risk mitigation:** Separation of concerns reduces blast radius of bugs and simplifies security auditing of the backend boundary.

---

## Implementation Notes

- **First steps:** Define and version the REST API contract (`/v1/` prefix); establish Docker Compose for local development with both services and a PostgreSQL instance; initialize Django project structure.
- **Dependencies:** ADR-002 (Authorization Model) must be resolved to inform Django authentication and DRF permission classes. ADR-008 (Backend Framework Selection) documents the Django/DRF decision.
- **Success criteria:** All MVP functionality is accessible via the documented API endpoints; frontend can be developed against a backend stub.
- **Migration path:** N/A — greenfield project.

---

## Consequences

### Positive Consequences
- Frontend and backend can be developed in parallel once contracts are established
- Clear security boundary — all authorization enforced at the API layer
- Deployment flexibility (containers can be moved to any host or orchestrator)

### Negative Consequences / Trade-offs
- Requires API versioning discipline from day one
- Cross-origin configuration (CORS) must be explicitly managed
- Integration tests must span the API boundary rather than calling functions directly
