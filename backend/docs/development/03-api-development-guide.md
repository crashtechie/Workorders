# API Development Guide

## API Contract Baseline
- base path pattern: `/api/v1/...`
- authenticated access required for all non-login endpoints
- error envelope must include: `code`, `message`, optional `details`, and `trace_id`

## Resource Domains
- customers
- workorders
- services (service definitions)
- workorder items and billing summaries
- inventory items and stock events
- reports and CSV export

## Endpoint Matrix

### Customers
- `POST /api/v1/customers`
- `GET /api/v1/customers`
- `GET /api/v1/customers/{id}`
- `PATCH /api/v1/customers/{id}`
- `DELETE /api/v1/customers/{id}`

Filters:
- `q`, `email`, `phone`

### Workorders
- `POST /api/v1/workorders`
- `GET /api/v1/workorders`
- `GET /api/v1/workorders/{id}`
- `PATCH /api/v1/workorders/{id}`
- `DELETE /api/v1/workorders/{id}`
- `POST /api/v1/workorders/{id}/status`
- `POST /api/v1/workorders/{id}/assign`

Filters:
- `customer_id`, `status`, `service_definition_id`, `device_type`, `date_received_from`, `date_received_to`

### Services (Service Module)
- `POST /api/v1/services`
- `GET /api/v1/services`
- `GET /api/v1/services/{id}`
- `PATCH /api/v1/services/{id}`
- `DELETE /api/v1/services/{id}`

Filters:
- `q`, `is_active`, `category`

### Billing
- `POST /api/v1/workorders/{id}/items`
- `PATCH /api/v1/workorders/{id}/items/{itemId}`
- `DELETE /api/v1/workorders/{id}/items/{itemId}`
- `GET /api/v1/workorders/{id}/billing-summary`
- `PATCH /api/v1/workorders/{id}/billing-mode`
- `POST /api/v1/workorders/{id}/receipt`
- `POST /api/v1/workorders/{id}/invoice`

### Inventory
- `POST /api/v1/inventory/items`
- `GET /api/v1/inventory/items`
- `GET /api/v1/inventory/items/{id}`
- `PATCH /api/v1/inventory/items/{id}`
- `DELETE /api/v1/inventory/items/{id}`
- `POST /api/v1/inventory/stock-events`
- `GET /api/v1/inventory/stock-events`

### Reports
- `GET /api/v1/reports/workorders`
- `GET /api/v1/reports/sales`
- `GET /api/v1/reports/inventory`
- `GET /api/v1/reports/customers`
- `GET /api/v1/reports/{reportType}/export?format=csv`

## Authorization Rules
- enforce role restrictions at view and object-action levels
- admin-only actions should be explicit in policy checks
- admin override actions must emit audit events with reason

## Request Validation Rules
- required fields must be validated server-side regardless of UI checks
- service selection must reference active service definitions unless override applies
- billing lines cannot have negative monetary values
- `check_number` and `card_transaction_id` must be non-empty when provided
- inventory stock events require `reason` and `actor_user_id`

## Response and Error Semantics
HTTP status usage:
- `400` validation format errors
- `401` unauthenticated
- `403` unauthorized by role/policy
- `404` resource not found
- `409` state conflict or concurrent update conflict
- `422` semantic validation failure
- `500` internal error

## Pagination and Sorting
List endpoints should support:
- `page`
- `page_size`
- `sort_by`
- `sort_order`

## API Testing Requirements
- endpoint contract tests
- role matrix tests per action
- filter and sorting tests
- error envelope conformance tests
- idempotency/concurrency tests where applicable
