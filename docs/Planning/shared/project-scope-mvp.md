# Project Scope: Workorders MVP

## Objective
Deliver a usable first release of the Workorders system for a small computer repair and sales business to manage customers, workorders, itemized billing, and basic inventory workflows.

## Problem Statement
Current operations require consistent tracking for:
- Customer intake
- Device and issue documentation
- Workorder lifecycle
- Billing line items and totals
- Inventory usage for parts and devices

## Roles
- Sales Staff (`sales_staff`): customer intake, sales workorders, billing, status updates
- Technician (`technician`): device/service execution, technician notes, parts usage, status updates
- Administrator (`admin`): user/role management, inventory administration, reporting access

## MVP In Scope
- Authentication and role-based authorization for `sales_staff`, `technician`, and `admin`
- Customer management
  - Create, view, edit, delete, and search customer records
- Workorder management
  - Create, view, edit, delete, and search workorders
  - Track lifecycle status, assignment, and key dates
- Service classification
  - Configurable Service Module managed by the business (add, edit, activate/deactivate, remove)
  - Workorders select service definitions from business-configured service catalog
  - Service location captured separately (on-site, in-shop, other)
- Device details capture
  - Device metadata and issue description
- Billing
  - Itemized lines for parts, labor, services, and sales
  - Subtotal, sales tax, and total
  - Standard sales workflow with bill now (receipt) and bill later (invoice)
  - Optional payment metadata capture: check_number and card_transaction_id (external reference only)
  - Partial payments are required in MVP
- Inventory
  - Track SKUs, stock on hand, workorder consumption of parts, and inventory item removal/deactivation
- Reporting
  - On-screen operational reports and CSV export for MVP
- Responsive web experience
  - Desktop, tablet, and mobile support
- Data protection baseline
  - Sensitive field controls, audit events, and backup policy

## MVP Out of Scope
- Third-party payment gateway integration
- Public API for external systems
- Advanced export formats (PDF, XLSX)
- Full legal compliance automation for every jurisdiction

## Candidate Post-MVP Scope
### Phase 2
- Email notifications for customer updates
- Low-stock notification workflows
- Expanded reporting with saved filters
- PDF/XLSX exports

### Phase 3
- External integrations (CRM/accounting)
- Public/internal integration API
- Advanced analytics and forecasting

## Success Metrics
- 100% of active workorders tracked in system
- Workorder creation completes in under 3 minutes for standard intake
- Search/filter returns expected results for customer and workorder lists
- Billing totals are reproducible and correct for tested tax scenarios
- Zero plaintext storage of protected sensitive fields

## Risks and Mitigations
- Scope creep: enforce MVP out-of-scope gate in release plan
- Sensitive data handling mistakes: encryption, role restrictions, and audit logging
- Reporting complexity: ship CSV-first, expand formats post-MVP
- Data quality issues: add field validation and mandatory key fields

## Assumptions
- Single business organization in MVP (no multi-tenant support)
- Sales tax model is a single configured rate per jurisdiction context for MVP
- Staff users are provisioned by administrators

## Resolved Decisions
- The app must not ship with default built-in service definitions; services are configured by the business through a Service Module.
- Temporary device credential notes should not auto-expire on completion.
- Partial payments are required in MVP.