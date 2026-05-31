# Requirements Traceability Matrix

## Source
- Source document: idea.log

## Requirement IDs

| ID | Requirement Summary | Source Lines | Planned Document(s) | Validation Method |
| --- | --- | --- | --- | --- |
| R1 | Track customer repairs and sales workorders | 1 | project-scope-mvp.md, backend-data-model.md | End-to-end workflow test |
| R2 | Capture customer information fields | 4-9 | backend-data-model.md, frontend-workorder-ux.md | Field-level validation tests |
| R3 | Capture service requested categories | 10-35 | architecture-decisions.md, backend-api-spec.md, backend-data-model.md, frontend-workorder-ux.md | Service field mapping tests |
| R4 | Capture device information fields | 36-45 | backend-data-model.md, frontend-workorder-ux.md | Required/optional field tests |
| R5 | Capture issue description | 46 | backend-data-model.md, frontend-workorder-ux.md | Form/API validation |
| R6 | Track workorder status and dates | 47-50 | backend-data-model.md, backend-api-spec.md | Lifecycle transition tests |
| R7 | Itemized billing for parts/labor/services/sales/tax/total and optional payment references | 51-56 | backend-billing-tax-rules.md, backend-api-spec.md, backend-data-model.md, frontend-workorder-ux.md | Billing calculation + payment metadata validation tests |
| R8 | User auth and role authorization | 59-61 | architecture-decisions.md, frontend-role-based-ui.md, backend-api-spec.md | Role access test matrix |
| R9 | Customer CRUD (including delete) and search/filter | 62-64 | backend-api-spec.md, frontend-workorder-ux.md | CRUD + query tests |
| R10 | Workorder CRUD (including delete) and search/filter | 65-68 | backend-api-spec.md, frontend-workorder-ux.md | CRUD + query tests |
| R11 | Inventory tracking, add/update/remove, and low stock | 69-72 | backend-inventory-flow.md, backend-api-spec.md, frontend-dashboard-reports.md | Stock event and threshold tests |
| R12 | Reporting and exports | 73-75 | frontend-dashboard-reports.md, release-plan.md | Report output verification |
| R13 | Multi-device accessibility | 76-77 | frontend-responsive-guidelines.md | Responsive checklist |
| R14 | User-friendly interface | 78-79 | frontend-workorder-ux.md, frontend-role-based-ui.md | UX acceptance criteria |
| R15 | Data security and privacy | 80-83 | architecture-decisions.md, backend-api-spec.md | Security checklist |
| R16 | Optional third-party integrations | 84-86 | project-scope-mvp.md, release-plan.md | Scope gate review |
| R17 | Optional API integrations | 87 | project-scope-mvp.md, release-plan.md | Scope gate review |

## Clarifications Applied
- Service handling is implemented via a configurable Service Module (`service_definition`) plus `service_location`.
- The application does not ship with hardcoded default services; the business manages service definitions.
- Sensitive credentials are treated as prohibited for plaintext storage.
- CSV is MVP export format; PDF/XLSX deferred.

## Coverage Check
- All requirements in idea.log are mapped to one or more planning docs.
- Deferred requirements are explicitly captured in scope and release planning.