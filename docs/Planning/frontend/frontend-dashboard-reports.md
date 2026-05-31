# Frontend Dashboard and Reports (MVP)

## Problem Statement
Operational users need quick visibility into workorders, sales, inventory, and customer activity with filterable report views and export capability.

## User Impact
- Faster daily oversight
- Better decision making on workload and inventory
- Easier sharing of operational snapshots

## MVP Report Types
- Workorders by status/date/assignee
- Sales summary by period
- Inventory levels and low-stock list
- Customer activity summary

## Filter Controls
- Date range
- Status
- Service offering (service definition)
- Service location
- Assignee
- Customer search

## Data Presentation
- Table-first layout on desktop
- Card/list adaptation on mobile
- Column sorting where applicable

## Export Strategy (MVP)
- CSV export only
- Export uses currently applied filters
- Export action displays success/error feedback

## Empty and Error States
- Empty state with guidance text and clear next action
- Error state with retry action and minimal technical detail

## Dependencies
- backend-api-spec.md report endpoints
- release-plan.md scope gate for export formats

## Acceptance Criteria
- Users can filter each report type by defined controls.
- CSV export contains filtered dataset and expected columns.
- Report views are responsive and usable on supported devices.
- Empty/error states are informative and non-blocking.