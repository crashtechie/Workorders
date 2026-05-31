# Testing and Quality Gates

## Purpose
Define the backend verification strategy required to prove MVP correctness, security, and readiness.

## Test Pyramid (Backend)
- unit tests: pure business rules, calculations, state transitions
- integration tests: API to DB behavior, transactional integrity
- contract tests: request/response schema and error envelope conformance
- authorization tests: role matrix and forbidden action validation
- smoke tests: runtime health and critical endpoint readiness

## Required Test Coverage Areas

### Customers and Workorders
- CRUD success paths
- validation failures for required fields
- search/filter behavior and pagination
- status transition policy enforcement
- assignment and role restrictions

### Service Module
- service CRUD behavior
- active/inactive service selection validation
- no hardcoded default service dependency

### Billing
- line item validation by type
- deterministic subtotal/tax/total calculations
- rounding edge cases
- estimate/invoice state transition lock behavior
- partial payments and payment status transitions
- `check_number` and `card_transaction_id` validation

### Inventory
- purchase/consume/adjust event mutation correctness
- transaction atomicity between stock mutation and stock event creation
- low-stock threshold behavior
- workorder-linked consumption integrity

### Security and Audit
- auth required on protected endpoints
- role matrix enforcement (`sales_staff`, `technician`, `admin`)
- sensitive data protection rules
- required audit event generation and payload completeness

## Error Contract Verification
Every endpoint family should include tests for:
- 400 invalid payload
- 401 unauthenticated access
- 403 forbidden by role
- 404 missing resource
- 409 conflict/state race
- 422 semantic validation failure

## Quality Gates by Milestone

### M1: Foundation and Contracts
- API contract baselines approved
- requirement mappings established

### M2: Core CRUD and Lifecycle
- CRUD and lifecycle tests pass
- role checks pass for protected actions

### M3: Billing and Inventory Core
- billing deterministic test matrix passes
- inventory integrity and race handling tests pass

### M4: Reporting and Export
- report endpoint correctness validated
- CSV export format and content checks pass

### M5: Hardening and Readiness
- security checklist completed
- backup and restore evidence completed
- release readiness sign-off complete

## CI Expectations
- run test suite on every merge request
- fail build on test, lint, or migration check failure
- publish test report artifacts with requirement ID tags

## Evidence Recording
For each completed requirement:
- reference requirement ID
- list validating test names
- provide pass/fail evidence location
- include regression notes if behavior changed
