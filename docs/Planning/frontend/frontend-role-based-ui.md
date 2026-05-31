# Frontend Role-Based UI Behavior (MVP)

## Problem Statement
Different user roles need targeted UI actions and visibility, while maintaining clear UX and preventing unauthorized modifications.

## Roles
- sales_staff
- technician
- admin

## Role Matrix

### sales_staff
- Can create and edit customers
- Can create and edit workorders
- Can manage billing lines within allowed workflow state
- Can request deletion for draft customers/workorders per policy
- Cannot manage Service Module definitions
- Cannot access administrative user/role management screens

### technician
- Can view assigned and relevant workorders
- Can update status, technician notes, and parts usage actions
- Cannot perform user administration
- Limited billing edit permissions based on workflow state
- Cannot manage Service Module definitions

### admin
- Full visibility across records
- User/role/inventory administration capabilities
- Full Service Module administration (add/edit/activate/deactivate/remove)
- Override actions where explicitly allowed and audited
- Final authority for delete/remove operations where required

## UI Visibility Rules
- Hide unavailable actions rather than showing broken flows.
- Show informative messaging where action is restricted by role/state.
- Mark read-only fields when role lacks edit permission.

## State-Dependent Rules
- Completed workorders restrict edits for non-admin roles.
- Finalized invoices restrict billing edits for non-admin roles.
- Deletion of finalized or historically referenced records is blocked or converted to soft-delete per policy.

## Unauthorized UX Patterns
- Route guards for protected pages
- Disabled controls with explanatory tooltip/message for contextual restrictions
- Fallback error handling for backend 403 responses

## Dependencies
- architecture-decisions.md for RBAC model
- backend-api-spec.md for authorization behavior

## Acceptance Criteria
- UI action availability matches role matrix and state rules.
- Unauthorized actions are blocked in UI and by backend.
- Users receive clear feedback when access is restricted.