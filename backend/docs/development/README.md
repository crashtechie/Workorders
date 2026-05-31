# Backend Development Documentation

## Purpose
This folder contains implementation-ready backend development guidance derived from the planning artifacts in `docs/Planning`.

It is intended for day-to-day engineering execution and includes:
- architecture and scope
- local environment and setup
- API implementation guidance
- domain/data model implementation details
- billing and inventory business rules
- security and audit baseline
- testing and release traceability

## Source Planning Documents
Primary references:
- `docs/Planning/shared/project-scope-mvp.md`
- `docs/Planning/shared/architecture-decisions.md`
- `docs/Planning/shared/requirements-traceability.md`
- `docs/Planning/shared/release-plan.md`
- `docs/Planning/backend/backend-api-spec.md`
- `docs/Planning/backend/backend-data-model.md`
- `docs/Planning/backend/backend-billing-tax-rules.md`
- `docs/Planning/backend/backend-inventory-flow.md`

## Document Index
1. `01-development-overview.md`
2. `02-environment-and-setup.md`
3. `03-api-development-guide.md`
4. `04-data-model-and-lifecycle.md`
5. `05-billing-and-tax-implementation.md`
6. `06-inventory-and-stock-events.md`
7. `07-security-audit-and-backup.md`
8. `08-testing-and-quality-gates.md`
9. `09-traceability-and-release-execution.md`

## Usage Guidance
- Start with `01-development-overview.md` for boundaries and architecture.
- Use `03-api-development-guide.md` and `04-data-model-and-lifecycle.md` before writing endpoints.
- Implement billing and inventory only with rules in documents 5 and 6.
- Validate with document 8 and update requirement mapping in document 9.

## Maintenance Rules
- Keep API and data-model docs in sync with actual implementation changes.
- If scope changes, update planning docs first, then this folder.
- Every milestone completion should update validation evidence in the traceability document.
