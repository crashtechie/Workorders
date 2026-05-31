# Release Plan: MVP

## Release Objective
Ship a stable MVP that supports customer intake, workorder execution, billing, inventory basics, and reporting with role-aware access.

## Milestones

### M1: Foundation and Contracts
- Finalize shared scope, ADRs, and traceability matrix
- Finalize backend API and data model contracts
- Finalize frontend role matrix and workorder flow
- Finalize Service Module contracts and role permissions

#### Exit Criteria
- Shared docs approved
- API contract baseline approved
- MVP scope freeze enacted

### M2: Core CRUD and Lifecycle
- Customer CRUD (including delete) and search
- Workorder CRUD (including delete) and lifecycle transitions
- Service Module CRUD (add/edit/deactivate/remove) and workorder service selection
- Date/status handling and assignment support

#### Exit Criteria
- CRUD acceptance tests pass
- Role restrictions enforced for protected actions
- Workorder service selections resolve from business-configured service definitions

### M3: Billing and Inventory Core
- Itemized billing lines and total calculations, including standard sales mode support
- Optional payment metadata capture in billing flows (`check_number`, `card_transaction_id`)
- Inventory item setup and stock movement events
- Workorder-to-parts consumption linkage

#### Exit Criteria
- Billing test cases pass for tax/rounding scenarios
- Billing metadata validation covers optional payment reference fields
- Inventory stock event integrity verified

### M4: Reporting and Responsive UX
- Dashboard/report list views
- CSV export for operational reports
- Responsive behavior for mobile/tablet/desktop

#### Exit Criteria
- Report filters and exports validated
- Responsive QA checklist passes

### M5: Hardening and Readiness
- Security baseline checks
- Backup/restore verification
- Documentation and operational handoff

#### Exit Criteria
- Security checklist signed off
- Backup restore drill completed
- Known risks accepted or mitigated

## Dependencies and Sequencing
- Shared scope and architecture docs are prerequisites for implementation.
- Backend API/data model decisions unblock frontend integration.
- Billing and inventory logic should be completed before final report validation.

## Definition of Done
- All MVP in-scope features implemented and tested.
- All critical defects resolved.
- Traceability matrix requirements marked validated.
- Deferred items documented with phase target.

## Scope Gates
- MVP does not include payment processor integration.
- MVP does not include external system API integration.
- MVP export format is CSV only.

## Rollout and Backout
- Rollout: staged deployment, smoke test, then production enablement.
- Backout: revert to previous stable deployment and restore backup if needed.

## Risk Register (MVP)
- Data sensitivity handling errors
- Billing miscalculation regressions
- Inventory event inconsistency
- Delayed scope freeze leading to schedule slip

## Reporting Cadence
- Weekly milestone review
- Requirement traceability updates after each milestone
- Release readiness review before production go-live