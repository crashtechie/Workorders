# Planning Index

## Purpose
Central index of planning artifacts for the Workorders MVP.

## Shared
- project-scope-mvp.md
- architecture-decisions.md
- requirements-traceability.md
- release-plan.md
- planning-index.md

## Internal Artifacts
- plan-workordersDevelopmentPlanningDocs.prompt.md

## Backend
- ../backend/backend-api-spec.md
- ../backend/backend-data-model.md
- ../backend/backend-billing-tax-rules.md
- ../backend/backend-inventory-flow.md

## Frontend
- ../frontend/frontend-workorder-ux.md
- ../frontend/frontend-dashboard-reports.md
- ../frontend/frontend-responsive-guidelines.md
- ../frontend/frontend-role-based-ui.md

## Dependency Order
1. project-scope-mvp.md
2. architecture-decisions.md
3. requirements-traceability.md
4. backend-api-spec.md + backend-data-model.md
5. backend-billing-tax-rules.md + backend-inventory-flow.md
6. frontend-workorder-ux.md + frontend-role-based-ui.md
7. frontend-dashboard-reports.md + frontend-responsive-guidelines.md
8. release-plan.md

## Scope Gates
- Payment integration deferred post-MVP.
- External integration API deferred post-MVP.
- CSV is the only MVP export format.

## Handoff Notes
- Implementation should begin from shared decisions and API/data contracts.
- Traceability updates are required when requirements or scope changes.