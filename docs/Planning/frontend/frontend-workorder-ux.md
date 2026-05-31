# Frontend Workorder UX Flow (MVP)

## Problem Statement
Sales staff and technicians need a fast, consistent workflow to create and update workorders with complete intake data and billing-ready records.

## User Impact
- Reduces intake errors
- Improves handoff between sales and technicians
- Enables reliable downstream billing and reporting

## Primary Screens
- Workorder list
- New workorder wizard/form
- Workorder detail/edit view
- Customer quick create/edit modal
- Workorder and customer delete confirmation dialog
- Service Module management screens (admin)

## Proposed UX Flow
1. Start workorder from list page.
2. Enter/select customer.
3. Select service type and service location.
4. Capture device details.
5. Capture issue description and intake notes.
6. Set dates/status and assignment.
7. Select billing mode for standard sales when applicable (bill now receipt or bill later invoice).
8. Add itemized billing lines (optional at intake, required before completion).
9. Optionally delete draft records with role-allowed confirmation.
10. Save draft or submit.

## Form Field Rules
### Required at Creation
- customer
- service_definition_id
- service_location
- device_type
- manufacturer
- model
- issue_description
- status (default: received)
- date_received

### Service Type Selection Guidance
- Populate service options from Service Module configuration only.
- Do not hardcode default service options in the client.
- Show only active service definitions for standard users.
- Allow admin workflows to manage add/edit/deactivate/remove actions.
- Present service location separately: on-site, in-shop, other.

### Optional at Creation
- serial_number
- accessories_included
- operating_system
- software_installed
- estimated_completion_date
- assigned_technician

## Conditional Behavior
- date_completed enabled only when status = completed.
- labor-specific fields appear only when billing item type = labor.
- check_number field appears only when payment method is check-based/manual.
- card_transaction_id field appears for card/manual-entry flows and is labeled as third-party reference.
- role-based action visibility depends on current user role.

## Validation Messaging
- Inline error per field
- Summary banner for form-level failures
- Preserve user input on validation failure

## Save Draft vs Submit
- Save Draft: allows incomplete billing and optional secondary fields.
- Submit/Finalize: enforces completion rules for required workflow fields.

## Delete Behavior
- Customer/workorder deletion requires confirmation and role authorization.
- Use soft-delete behavior messaging if records are preserved for history.

## Dependencies on Backend/Shared
- backend-api-spec.md for payload contracts
- backend-data-model.md for field definitions and status constraints
- architecture-decisions.md for role behavior and sensitive data policy

## Acceptance Criteria
- User can create a valid workorder in one pass.
- Validation errors are clear and actionable.
- Status/date field constraints match backend lifecycle rules.
- Role restrictions are visible in UI and enforced by backend.

## Accessibility Notes
- Keyboard-navigable forms
- Label association for all controls
- Error messages announced for assistive technologies