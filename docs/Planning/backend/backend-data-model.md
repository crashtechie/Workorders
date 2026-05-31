# Backend Data Model (MVP)

## Objective
Define normalized entities, required fields, lifecycle states, and constraints for MVP persistence.

## Core Entities

### customer
#### Required Fields
- id
- full_name
- contact_number

#### Optional Fields
- company_name
- email
- physical_address

### workorder
#### Required Fields
- id
- workorder_number
- customer_id
- service_definition_id
- service_location
- issue_description
- status
- date_received

#### Optional Fields
- estimated_completion_date
- date_completed
- assigned_technician_id
- internal_notes
- customer_notes

### device
#### Required Fields
- id
- workorder_id
- device_type
- manufacturer
- model

#### Optional Fields
- serial_number
- accessories_included
- condition
- operating_system
- software_installed
- credential_note_ref

### workorder_item
#### Required Fields
- id
- workorder_id
- item_type (parts, labor, services)
- description
- quantity
- unit_price
- line_total

#### Optional Fields
- sku
- labor_hours
- hourly_rate

### service_definition
#### Required Fields
- id
- code
- name
- is_active

#### Optional Fields
- category
- description
- default_price
- billing_mode_default
- allow_partial_payment
- display_order

### billing_summary
#### Required Fields
- workorder_id
- subtotal
- tax_amount
- total

#### Optional Fields
- payment_status
- payment_method
- billing_mode
- check_number
- card_transaction_id

### inventory_item
#### Required Fields
- id
- sku
- description
- stock_on_hand

#### Optional Fields
- cost_price
- sell_price
- reorder_point
- reorder_quantity
- supplier_name

### stock_event
#### Required Fields
- id
- inventory_item_id
- event_type (purchase, consume, adjust)
- quantity_delta
- reason
- actor_user_id
- created_at

#### Optional Fields
- workorder_id

## Service Module Guidance
- Workorders must reference `service_definition_id` from business-configured services.
- Service definitions are business-managed and not hardcoded by the application.
- Recommended deletion behavior is deactivate/archival when historical workorders reference a service.
- `service_location` remains separate and should support: on_site, in_shop, other.

## Billing Mode Guidance
- billing_mode values for standard sales workflow: bill_now_receipt, bill_later_invoice.

## Relationships
- customer 1:N workorder
- service_definition 1:N workorder
- workorder 1:1 device
- workorder 1:N workorder_item
- inventory_item 1:N stock_event
- workorder 1:N stock_event (for part consumption linkage)

## Workorder Status Lifecycle
### Allowed States
- received
- in_progress
- on_hold
- completed

### Transition Guidance
- received -> in_progress
- in_progress -> on_hold
- on_hold -> in_progress
- in_progress -> completed

## Constraints
- workorder_number is unique.
- sku is unique for inventory items.
- service_definition.code is unique.
- line_total must equal quantity * unit_price for non-labor item types.
- labor lines require labor_hours and hourly_rate.
- total must equal subtotal + tax_amount.
- date_completed must be null unless status is completed.
- workorder.service_definition_id must reference an active service unless admin override is used.

## Indexing Strategy
- customer(full_name, company_name, email)
- service_definition(code, name, is_active)
- workorder(status, date_received, customer_id, service_definition_id)
- device(serial_number)
- inventory_item(sku, description)
- stock_event(inventory_item_id, created_at)

## Sensitive Data Notes
- Serial numbers are treated as protected operational identifiers.
- Device credential notes are temporary, role-restricted, and must not be stored as plaintext password fields.

## Validation Plan
- Entity schema validation tests
- Relationship integrity tests
- Status transition tests
- Constraint and computed-value tests