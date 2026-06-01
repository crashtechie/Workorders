# Feature: API v1 Routing and Contract Baseline

## Feature Overview
Introduce a stable API routing structure under `/api/v1` and establish foundational API contract behavior.

Why this matters:
- Gives frontend and QA a stable route namespace.
- Avoids route drift as more apps are introduced.
- Preserves health check behavior for runtime monitoring.

## User Stories

### Story 1
- As a frontend developer,
- I want all backend endpoints under `/api/v1`,
- So that integration remains stable over time.

### Story 2
- As an operations engineer,
- I want health endpoint behavior unchanged,
- So that container readiness/liveness checks continue to work.

### Story 3
- As a backend developer,
- I want domain routes split by app modules,
- So that ownership and maintenance are clear.

## Acceptance Criteria

### Criterion 1
- Given app starts,
- When routing is inspected,
- Then customers and workorders route trees are mounted under `/api/v1`.

### Criterion 2
- Given health endpoint is requested,
- When `GET /api/v1/health/` is called,
- Then service returns healthy status response.

### Criterion 3
- Given domain app URL modules exist,
- When a new endpoint is added to app URL config,
- Then no root URL refactor is needed beyond include registration.

## Implementation Plan

### Scope
- Ticket mapping: BE-M1-02
- Requirement mapping: R8

### Target Files
- `backend/config/urls.py`
- `backend/apps/customers/urls.py` (new)
- `backend/apps/workorders/urls.py` (new)

### Tasks
1. Keep health route in root config.
2. Register `customers` and `workorders` app URLs with `/api/v1` prefix.
3. Add placeholders for future domains (`billing`, `inventory`, `reports`) as commented include points or TODO notes.
4. Ensure route naming conventions are consistent and explicit.

## Test Plan
- URL reverse and resolve tests for mounted routes.
- Health route regression test.
- 404 contract test for unknown route under `/api/v1`.

## Risks and Mitigation
- Risk: Breaking existing health probe path.
  - Mitigation: Preserve endpoint path and response shape.
- Risk: Inconsistent domain URL naming.
  - Mitigation: Define naming convention in each app `urls.py`.

## Definition of Done
- API v1 routing baseline merged.
- Domain route includes for customers/workorders are active.
- Health route unchanged and tested.
