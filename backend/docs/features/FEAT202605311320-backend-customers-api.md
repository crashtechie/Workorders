# Feature: Customers API (CRUD and Filters)

## Feature Overview
Implement customer API endpoints with role-aware access, input validation, filtering, and lifecycle-safe delete behavior.

Why this matters:
- Enables customer intake and lookup for workorder creation.
- Creates first production API surface for frontend integration.
- Validates shared API patterns (auth, pagination, error contracts).

## User Stories

### Story 1
- As a sales staff user,
- I want to create and update customer records,
- So that workorders can be tracked correctly.

### Story 2
- As a technician,
- I want to search customers by name/email/phone,
- So that I can quickly find related workorders.

### Story 3
- As an admin,
- I want lifecycle-safe delete behavior,
- So that historical references are not corrupted.

## Acceptance Criteria

### Criterion 1
- Given authenticated user with allowed role,
- When customer CRUD endpoints are used,
- Then operations succeed with valid payloads and return expected status codes.

### Criterion 2
- Given filters (`q`, `email`, `phone`) are provided,
- When list endpoint is called,
- Then results are filtered correctly and paginated.

### Criterion 3
- Given customer has linked workorders,
- When delete is requested,
- Then API enforces lifecycle-safe delete policy (block or archive strategy).

## Implementation Plan

### Scope
- Ticket mapping: BE-M2-02
- Requirement mapping: R1, R9

### Target Files
- `backend/apps/customers/serializers.py` (new)
- `backend/apps/customers/views.py` (new)
- `backend/apps/customers/urls.py` (new)
- `backend/apps/customers/tests/test_api.py` (new)

### Endpoints
- `POST /api/v1/customers`
- `GET /api/v1/customers`
- `GET /api/v1/customers/{id}`
- `PATCH /api/v1/customers/{id}`
- `DELETE /api/v1/customers/{id}`

### Validation Rules
- Required on create: `full_name`, `contact_number`.
- Optional: `company_name`, `email`, `physical_address`.
- Server-side validation required even if frontend validates.

### Role Expectations
- `sales_staff`: create/read/update.
- `technician`: read/search.
- `admin`: full CRUD including delete path.

## Test Plan
- CRUD success tests by role.
- Required field validation tests (`400/422` as implemented contract).
- Unauthorized/forbidden tests (`401`, `403`).
- Missing customer tests (`404`).
- Filter and pagination tests.
- Delete safety behavior tests.

## Risks and Mitigation
- Risk: Hard delete causes orphan references.
  - Mitigation: Implement safe delete policy before exposing delete endpoint.
- Risk: Inconsistent filter behavior.
  - Mitigation: Define and test deterministic filter precedence.

## Definition of Done
- All customer endpoints implemented and mounted.
- Filter and role matrix tests pass.
- Delete behavior is safe and documented.
