# Backend API Spec (MVP)

## Objective
Define the MVP backend API surface and contract expectations for customer, workorder, billing, inventory, and reporting workflows.

## Scope
- Internal API for frontend consumption
- Role-protected endpoints
- Search/filter support for key list views
- Path convention: all endpoint references in planning docs use `/api/&lt;version id&gt;/...` (example: `/api/v1/...`).

## Non-Goals
- Public integration API in MVP
- Webhook/event streaming in MVP

## Authentication and Authorization
- Authenticated access required for all non-login endpoints.
- Role enforcement:
  - sales_staff: customer/workorder create/update, billing updates within allowed rules
  - technician: workorder status/notes, parts consumption updates
  - admin: user/role/inventory administration and full reporting access

## Resource Model
- customers
- workorders
- service_definitions
- workorder_items (parts, labor, services, sales)
- inventory_items
- stock_events
- reports

## Endpoint Matrix

### Customers
- POST /api/&lt;version id&gt;/customers
- GET /api/&lt;version id&gt;/customers
- GET /api/&lt;version id&gt;/customers/{id}
- PATCH /api/&lt;version id&gt;/customers/{id}
- DELETE /api/&lt;version id&gt;/customers/{id}

#### Filters
- q (name/company/contact)
- email
- phone

### Workorders
- POST /api/&lt;version id&gt;/workorders
- GET /api/&lt;version id&gt;/workorders
- GET /api/&lt;version id&gt;/workorders/{id}
- PATCH /api/&lt;version id&gt;/workorders/{id}
- DELETE /api/&lt;version id&gt;/workorders/{id}
- POST /api/&lt;version id&gt;/workorders/{id}/status
- POST /api/&lt;version id&gt;/workorders/{id}/assign

#### Filters
- customer_id
- status
- service_definition_id
- device_type
- date_received_from
- date_received_to

### Service Module
- POST /api/&lt;version id&gt;/services
- GET /api/&lt;version id&gt;/services
- GET /api/&lt;version id&gt;/services/{id}
- PATCH /api/&lt;version id&gt;/services/{id}
- DELETE /api/&lt;version id&gt;/services/{id}

#### Filters
- q (name/code)
- is_active
- category

### Billing
- POST /api/&lt;version id&gt;/workorders/{id}/items
- PATCH /api/&lt;version id&gt;/workorders/{id}/items/{itemId}
- DELETE /api/&lt;version id&gt;/workorders/{id}/items/{itemId}
- GET /api/&lt;version id&gt;/workorders/{id}/billing-summary
- PATCH /api/&lt;version id&gt;/workorders/{id}/billing-mode
- POST /api/&lt;version id&gt;/workorders/{id}/receipt
- POST /api/&lt;version id&gt;/workorders/{id}/invoice

#### Billing Payment Metadata (MVP)
- `check_number` may be accepted and recorded for check-based/manual payment flows.
- `card_transaction_id` may be accepted and recorded as an external reference from a third-party card processor.
- These fields are optional metadata only and do not imply in-app payment gateway processing.

### Inventory
- POST /api/&lt;version id&gt;/inventory/items
- GET /api/&lt;version id&gt;/inventory/items
- GET /api/&lt;version id&gt;/inventory/items/{id}
- PATCH /api/&lt;version id&gt;/inventory/items/{id}
- DELETE /api/&lt;version id&gt;/inventory/items/{id}
- POST /api/&lt;version id&gt;/inventory/stock-events
- GET /api/&lt;version id&gt;/inventory/stock-events

### Reports
- GET /api/&lt;version id&gt;/reports/workorders
- GET /api/&lt;version id&gt;/reports/sales
- GET /api/&lt;version id&gt;/reports/inventory
- GET /api/&lt;version id&gt;/reports/customers
- GET /api/&lt;version id&gt;/reports/{reportType}/export?format=csv

## Validation Rules
- Required fields enforced server-side for create/update operations.
- Workorder service selection must reference an active service definition unless admin override is explicitly used.
- Workorder status transitions must follow lifecycle rules.
- Billing lines must include valid type and non-negative monetary values.
- `check_number` and `card_transaction_id` must be non-empty when supplied.
- Inventory stock event must include reason and actor.

## Error Model
- 400: Validation error
- 401: Unauthenticated
- 403: Forbidden by role
- 404: Resource not found
- 409: Conflict (state transition or concurrent update conflict)
- 422: Semantic validation failure
- 500: Internal server error

### Error Response Shape
- code
- message
- details (optional)
- trace_id

## Pagination and Sorting
- List endpoints support:
  - page
  - page_size
  - sort_by
  - sort_order

## Security Notes
- Sensitive optional fields must never be returned in plaintext.
- Cardholder data (PAN/CVV) must never be accepted or persisted; only third-party transaction reference IDs are recorded.
- Audit log entries created for status changes, billing edits, and stock events.

## Validation Plan
- Contract tests per endpoint
- Role-based access tests per endpoint/action
- Query/filter correctness tests
- Error shape and status code conformance tests