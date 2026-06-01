# Feature: Core Domain Models and Migrations

## Feature Overview
Implement the initial data model and migrations for customer and workorder domains, including service definitions and device relationship.

Why this matters:
- Enables real persistence for API workflows.
- Encodes business constraints at DB/model level.
- Provides durable schema baseline for future billing and inventory integration.

## User Stories

### Story 1
- As a backend developer,
- I want normalized domain models with explicit relationships,
- So that business logic and API serialization remain consistent.

### Story 2
- As a product owner,
- I want unique and valid identifiers,
- So that records are traceable and conflicts are prevented.

### Story 3
- As a QA engineer,
- I want model constraints enforced automatically,
- So that invalid states are rejected reliably.

## Acceptance Criteria

### Criterion 1
- Given model migrations run on a clean DB,
- When `migrate` completes,
- Then all core tables and indexes are created without errors.

### Criterion 2
- Given duplicate `workorder_number` or duplicate `service_definition.code`,
- When records are created,
- Then persistence fails with integrity error.

### Criterion 3
- Given a completed workorder rule,
- When workorder status is not `completed`,
- Then `date_completed` must be null.

## Implementation Plan

### Scope
- Ticket mapping: BE-M2-01
- Requirement mapping: R1, R3, R6, R9, R10

### Target Files
- `backend/apps/customers/models.py` (new)
- `backend/apps/workorders/models.py` (new)
- `backend/apps/customers/migrations/*.py` (new)
- `backend/apps/workorders/migrations/*.py` (new)

### Minimum Entities for Sprint 1
- `customer`
- `service_definition`
- `workorder`
- `device`

### Required Constraints (Sprint 1)
- `workorder_number` unique.
- `service_definition.code` unique.
- FK integrity: `workorder.customer_id`, `workorder.service_definition_id`, `device.workorder_id`.
- Workorder status enum baseline: `received`, `in_progress`, `on_hold`, `completed`.
- `date_completed` null unless status `completed`.

### Index Baseline (Sprint 1)
- customer: full name/email/phone searchable fields.
- workorder: status/date/customer/service composite support.
- service definition: code/name/is_active.

## Test Plan
- Migration smoke test on clean DB.
- Model constraint tests for uniqueness and status/date rules.
- Relationship integrity tests for required foreign keys.

## Risks and Mitigation
- Risk: Over-modeling creates migration churn.
  - Mitigation: Limit scope to sprint entities only.
- Risk: Constraint logic split between model and serializer inconsistently.
  - Mitigation: Keep canonical business constraints in domain/model validation.

## Definition of Done
- Core models and migrations merged.
- Constraint tests pass.
- Schema supports customer and workorder API work.
