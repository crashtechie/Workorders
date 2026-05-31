# Architecture Decisions

## Context
The Workorders MVP requires coordinated backend/frontend implementation with secure handling of customer and device-related data, role-based access, and auditable lifecycle updates.

## Decision Log

## ADR-001: Application Architecture
- Decision: Use a layered web architecture with separate frontend and backend services.
- Rationale: Clear separation of concerns, easier iteration, and deployment flexibility.
- Consequences: Requires explicit API contracts and versioning discipline.

## ADR-002: Authorization Model
- Decision: Implement role-based access control with roles: sales_staff, technician, admin.
- Rationale: Matches business responsibilities and minimizes unauthorized changes.
- Consequences: Requires role matrix in frontend and endpoint authorization checks in backend.

## ADR-003: Workorder Domain Model
- Decision: Separate customer, workorder, workorder_item, inventory_item, and stock_event entities.
- Rationale: Supports searchability, itemized billing, and inventory traceability.
- Consequences: Requires transactional consistency for stock consumption and billing updates.

## ADR-004: Service Taxonomy
- Decision: Implement a configurable Service Module where service definitions are business-managed and referenced by workorders; keep service_location as a separate field.
- Rationale: Businesses must be able to add or remove services without code changes and avoid hardcoded defaults.
- Consequences: Requires service-definition CRUD, role controls for configuration, and referential validation from workorders.

## ADR-005: Sensitive Data Handling
- Decision: Prohibit persistent plaintext storage of device passwords/credentials.
- Rationale: Minimizes exposure risk and operational liability.
- Consequences: Use temporary secure note pattern with restricted visibility and expiration, or avoid storage entirely.

## ADR-006: Reporting and Export
- Decision: Ship CSV export in MVP; defer PDF/XLSX.
- Rationale: Faster delivery while meeting operational export needs.
- Consequences: Format expansion scheduled post-MVP.

## ADR-007: Integration Strategy
- Decision: Defer external integrations (payments, CRM/accounting API) until post-MVP.
- Rationale: Keep first release focused on core operations.
- Consequences: Add integration-ready extension points but no active integration implementation in MVP; allow optional external payment reference metadata (`check_number`, `card_transaction_id`) in billing records.

## Data Ownership
- Backend owns validation, persistence, business rules, and authorization.
- Frontend owns user interaction, presentation logic, and role-aware UX behavior.
- Shared ownership for API contracts and acceptance criteria.

## Audit and Logging Baseline
- Log authentication events and role-restricted actions.
- Log workorder status transitions and billing adjustments.
- Log inventory stock events with actor, reason, and timestamp.

## Backup and Recovery Baseline
- Daily backups for persistent data.
- Point-in-time restore strategy documented for production.
- Restore drills included in release readiness checklist.

## Non-Goals in MVP
- Multi-organization tenancy
- Offline-first client mode
- Real-time websocket updates

## Open Questions
- Required retention period for audit events.
- Final encryption strategy for sensitive optional fields.
- Expected target data volume for list/query performance sizing.