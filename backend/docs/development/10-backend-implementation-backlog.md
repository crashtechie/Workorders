# Backend Implementation Backlog (MVP)

## Purpose
Convert backend development guidance into an executable, ticket-sized backlog with file targets, acceptance criteria, and requirement traceability.

## Assumptions
- Current backend is scaffold-only (Django project with health endpoint).
- Implementation target is Django + DRF under `/api/v1`.
- Roles: `sales_staff`, `technician`, `admin`.

## Suggested Target Structure
Create the following app layout:

```text
backend/
  apps/
    authz/
    customers/
    workorders/
    billing/
    inventory/
    reports/
    audit/
```

Add shared modules as needed:

```text
backend/apps/common/
  errors.py
  pagination.py
  permissions.py
  responses.py
  filters.py
```

## Milestone Plan

## M1: Foundation and Contracts

### BE-M1-01: Configure DRF, JWT, and environment settings
- Requirements: R8, R15
- Target files:
  - `backend/config/settings.py`
  - `backend/requirements.txt`
  - `backend/.env.example` (new)
- Work:
  - Configure DRF defaults (auth, permissions, pagination).
  - Configure JWT signing via environment variable.
  - Add environment-driven DB and app flags (`APP_ENV`, `DATABASE_URL`, `AUDIT_LOG_ENABLED`, `TAX_RATE_DEFAULT`).
- Acceptance criteria:
  - App starts with env-driven config.
  - Unauthenticated protected endpoint returns `401`.

### BE-M1-02: Establish API v1 routing and health contract
- Requirements: R8
- Target files:
  - `backend/config/urls.py`
  - `backend/apps/*/urls.py` (new)
- Work:
  - Route domain APIs under `/api/v1/...`.
  - Keep health endpoint stable.
- Acceptance criteria:
  - Domain routes mounted and discoverable.
  - Existing health endpoint remains operational.

### BE-M1-03: Implement standard error envelope and trace id
- Requirements: R8, R15
- Target files:
  - `backend/apps/common/responses.py` (new)
  - `backend/apps/common/errors.py` (new)
  - `backend/apps/common/middleware.py` (new)
- Work:
  - Return error payload shape: `code`, `message`, `details?`, `trace_id`.
  - Propagate trace id in request lifecycle.
- Acceptance criteria:
  - `400/403/404/409/422/500` responses follow envelope contract.

### BE-M1-04: RBAC foundations and policy checks
- Requirements: R8
- Target files:
  - `backend/apps/authz/permissions.py` (new)
  - `backend/apps/common/permissions.py` (new)
- Work:
  - Implement role-based policy helpers for endpoint/action checks.
  - Add explicit admin override policy hooks (with reason requirement).
- Acceptance criteria:
  - Role matrix test skeleton exists and basic checks pass.

## M2: Core CRUD and Lifecycle

### BE-M2-01: Create core domain models and migrations
- Requirements: R1, R3, R6, R9, R10, R11
- Target files:
  - `backend/apps/customers/models.py` (new)
  - `backend/apps/workorders/models.py` (new)
  - `backend/apps/inventory/models.py` (new)
  - `backend/apps/billing/models.py` (new)
  - `backend/apps/*/migrations/*.py` (new)
- Work:
  - Implement entities and relations from data-model guidance.
  - Add uniqueness and immutability constraints.
  - Add indexes for search/filter performance.
- Acceptance criteria:
  - Migration applies cleanly.
  - DB constraints enforce required uniqueness and integrity rules.

### BE-M2-02: Customers API (CRUD + filters)
- Requirements: R1, R9
- Target files:
  - `backend/apps/customers/serializers.py` (new)
  - `backend/apps/customers/views.py` (new)
  - `backend/apps/customers/urls.py` (new)
  - `backend/apps/customers/tests/test_api.py` (new)
- Work:
  - Implement customer endpoints and query filters (`q`, `email`, `phone`).
  - Enforce lifecycle-safe delete behavior.
- Acceptance criteria:
  - CRUD and filter tests pass.

### BE-M2-03: Services API (service definition module)
- Requirements: R3, R10
- Target files:
  - `backend/apps/workorders/service_serializers.py` (new)
  - `backend/apps/workorders/service_views.py` (new)
  - `backend/apps/workorders/urls.py`
  - `backend/apps/workorders/tests/test_services_api.py` (new)
- Work:
  - Implement service definition CRUD and active/inactive behavior.
  - Prevent hardcoded defaults and enforce active selection rules.
- Acceptance criteria:
  - Inactive service cannot be selected without admin override.

### BE-M2-04: Workorders API + lifecycle transitions
- Requirements: R1, R6, R9, R10
- Target files:
  - `backend/apps/workorders/serializers.py` (new)
  - `backend/apps/workorders/views.py` (new)
  - `backend/apps/workorders/domain.py` (new)
  - `backend/apps/workorders/tests/test_lifecycle.py` (new)
- Work:
  - Implement workorder CRUD, assign endpoint, and status endpoint.
  - Enforce allowed state transitions and completion date rules.
  - Add filters for customer/status/service/device/date range.
- Acceptance criteria:
  - Invalid transition returns `409` or `422` per contract.
  - Assignment and lifecycle role restrictions pass tests.

## M3: Billing and Inventory Core

### BE-M3-01: Billing line item engine and totals
- Requirements: R7
- Target files:
  - `backend/apps/billing/serializers.py` (new)
  - `backend/apps/billing/views.py` (new)
  - `backend/apps/billing/domain.py` (new)
  - `backend/apps/billing/tests/test_calculations.py` (new)
- Work:
  - Implement line types (`parts`, `labor`, `services`, `sales`).
  - Compute `subtotal`, `tax_amount`, `total` deterministically.
  - Enforce 2-decimal half-up rounding and non-negative values.
- Acceptance criteria:
  - Deterministic calculation matrix and rounding edge tests pass.

### BE-M3-02: Billing state model and payment metadata
- Requirements: R7, R15
- Target files:
  - `backend/apps/billing/models.py`
  - `backend/apps/billing/domain.py`
  - `backend/apps/billing/tests/test_state_and_payment.py` (new)
- Work:
  - Implement states (`draft_estimate`, `approved_estimate`, `finalized_invoice`).
  - Lock finalized invoice edits except admin override.
  - Validate `check_number` and `card_transaction_id` semantics.
- Acceptance criteria:
  - Invalid state transitions rejected.
  - Metadata validations pass.

### BE-M3-03: Inventory item and stock event workflows
- Requirements: R11
- Target files:
  - `backend/apps/inventory/serializers.py` (new)
  - `backend/apps/inventory/views.py` (new)
  - `backend/apps/inventory/domain.py` (new)
  - `backend/apps/inventory/tests/test_stock_events.py` (new)
- Work:
  - Implement inventory CRUD and stock events (`purchase`, `consume`, `adjust`).
  - Enforce actor/reason mandatory fields and immutable SKU.
  - Support low-stock calculation (`stock_on_hand <= reorder_point`).
- Acceptance criteria:
  - Event mutation tests and low-stock threshold tests pass.

### BE-M3-04: Transactional integrity and concurrency controls
- Requirements: R11, R15
- Target files:
  - `backend/apps/inventory/domain.py`
  - `backend/apps/inventory/tests/test_concurrency.py` (new)
- Work:
  - Wrap stock mutation and event insert in one DB transaction.
  - Add race/conflict handling with retriable conflict response.
- Acceptance criteria:
  - Rollback tests and stale-update conflict tests pass.

## M4: Reporting and Export

### BE-M4-01: Report query endpoints
- Requirements: R12
- Target files:
  - `backend/apps/reports/views.py` (new)
  - `backend/apps/reports/serializers.py` (new)
  - `backend/apps/reports/urls.py` (new)
  - `backend/apps/reports/tests/test_reports_api.py` (new)
- Work:
  - Implement workorders, sales, inventory, customers report endpoints.
  - Support filter/pagination/sorting.
- Acceptance criteria:
  - Report endpoint correctness tests pass.

### BE-M4-02: CSV export pipeline
- Requirements: R12
- Target files:
  - `backend/apps/reports/exporters.py` (new)
  - `backend/apps/reports/tests/test_csv_export.py` (new)
- Work:
  - Implement `/api/v1/reports/{reportType}/export?format=csv`.
  - Validate headers, rows, and content formatting.
- Acceptance criteria:
  - CSV export tests pass for all report families.

## M5: Security, Audit, Readiness

### BE-M5-01: Audit event framework and coverage
- Requirements: R8, R15
- Target files:
  - `backend/apps/audit/models.py` (new)
  - `backend/apps/audit/services.py` (new)
  - `backend/apps/audit/tests/test_audit_events.py` (new)
- Work:
  - Log mandatory events for auth, restricted actions, lifecycle/billing/inventory changes, admin overrides.
  - Include actor, action, resource, timestamp, trace id, and before/after where applicable.
- Acceptance criteria:
  - Sensitive flow test suite verifies required audit events.

### BE-M5-02: Sensitive data handling guards
- Requirements: R15
- Target files:
  - `backend/apps/workorders/serializers.py`
  - `backend/apps/billing/serializers.py`
  - `backend/apps/*/tests/test_sensitive_data.py` (new)
- Work:
  - Block plaintext credential-like storage patterns.
  - Disallow PAN/CVV ingestion and persistence.
- Acceptance criteria:
  - Validation and persistence guard tests pass.

### BE-M5-03: Backup/restore operational runbook and drill evidence
- Requirements: R15
- Target files:
  - `backend/docs/development/07-security-audit-and-backup.md`
  - `docs/logs/backend/` (evidence files)
- Work:
  - Document daily backup procedure and restore process.
  - Execute restore drill and store evidence artifacts.
- Acceptance criteria:
  - Restore drill evidence recorded and reviewable.

## Cross-Cutting Tickets

### BE-X-01: Contract and error tests per endpoint family
- Requirements: R8, R15
- Target files:
  - `backend/apps/*/tests/test_error_contracts.py` (new)
- Work:
  - Verify `400/401/403/404/409/422` and envelope conformance.

### BE-X-02: Requirement traceability evidence updates
- Requirements: R1, R3, R6, R7, R8, R9, R10, R11, R12, R15
- Target files:
  - `backend/docs/development/09-traceability-and-release-execution.md`
  - `docs/Planning/shared/requirements-traceability.md`
- Work:
  - Map each implemented endpoint and test suite to requirement IDs.
  - Keep milestone status current.

## Execution Dependencies (Recommended Order)
1. BE-M1-01 -> BE-M1-04
2. BE-M2-01 -> (BE-M2-02, BE-M2-03, BE-M2-04)
3. BE-M3-01 -> BE-M3-02
4. BE-M3-03 -> BE-M3-04
5. BE-M4-01 -> BE-M4-02
6. BE-M5-01 and BE-M5-02
7. BE-M5-03 and BE-X-02

## Initial Sprint Cut (High Confidence)
If you want a fast first implementation sprint, start with:
1. BE-M1-01
2. BE-M1-02
3. BE-M2-01
4. BE-M2-02
5. BE-M2-04

This delivers secured core CRUD/lifecycle foundations and unlocks billing/inventory work in the next sprint.