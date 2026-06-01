# Feature: Workorders API, Assignment, and Lifecycle Transitions

## Feature Overview
Implement workorder CRUD plus lifecycle and assignment actions with strict transition rules and role enforcement.

Why this matters:
- Workorders are the core operational object in the platform.
- Lifecycle rules prevent invalid business states.
- Assignment and status controls define team workflow integrity.

## User Stories

### Story 1
- As a sales staff user,
- I want to create and update workorders,
- So that incoming customer requests are tracked from intake.

### Story 2
- As a technician,
- I want to move workorders through allowed statuses,
- So that job progress is accurately represented.

### Story 3
- As an admin,
- I want to assign technicians and perform overrides when policy allows,
- So that operational bottlenecks can be resolved safely.

## Acceptance Criteria

### Criterion 1
- Given valid payload and required references,
- When workorder CRUD endpoints are called,
- Then operation succeeds and response includes canonical workorder fields.

### Criterion 2
- Given current state and target state,
- When status transition endpoint is called,
- Then only allowed transitions are accepted.

### Criterion 3
- Given disallowed transition,
- When transition is attempted,
- Then API returns state conflict or semantic validation error per contract.

### Criterion 4
- Given assignment action is requested,
- When role policy is evaluated,
- Then only authorized roles may assign technician.

## Implementation Plan

### Scope
- Ticket mapping: BE-M2-04
- Requirement mapping: R1, R6, R9, R10

### Target Files
- `backend/apps/workorders/serializers.py` (new)
- `backend/apps/workorders/views.py` (new)
- `backend/apps/workorders/domain.py` (new)
- `backend/apps/workorders/urls.py` (new or updated)
- `backend/apps/workorders/tests/test_lifecycle.py` (new)

### Endpoints
- `POST /api/v1/workorders`
- `GET /api/v1/workorders`
- `GET /api/v1/workorders/{id}`
- `PATCH /api/v1/workorders/{id}`
- `DELETE /api/v1/workorders/{id}`
- `POST /api/v1/workorders/{id}/status`
- `POST /api/v1/workorders/{id}/assign`

### Required Transition Rules
- `received -> in_progress`
- `in_progress -> on_hold`
- `on_hold -> in_progress`
- `in_progress -> completed`

### Key Validation Rules
- Required create fields include:
  - `workorder_number`
  - `customer_id`
  - `service_definition_id`
  - `service_location`
  - `issue_description`
  - `status`
  - `date_received`
- `service_definition_id` must reference active service unless admin override path exists.
- `date_completed` must be null unless status is `completed`.

### Filters
- `customer_id`
- `status`
- `service_definition_id`
- `device_type`
- `date_received_from`
- `date_received_to`

## Test Plan
- CRUD tests by role.
- Allowed/disallowed lifecycle transition tests.
- Assignment policy tests.
- Filter/pagination/sorting tests.
- Error contract tests (`400/401/403/404/409/422`).

## Risks and Mitigation
- Risk: Transition logic scattered across serializer/view/model.
  - Mitigation: Centralize state transition policy in `domain.py`.
- Risk: Missing service-active validation creates invalid workorders.
  - Mitigation: Add explicit validation and tests for inactive service selection.

## Definition of Done
- Workorder endpoints, assignment, and status transitions implemented.
- Lifecycle and role tests pass.
- Filter and error contract behavior verified.
