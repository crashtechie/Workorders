# Backend Billing and Tax Rules (MVP)

## Objective
Define deterministic billing behavior for itemized workorder charges and totals.

## Line Item Categories
- parts
- labor
- services
- sales

## Line Item Rules
- parts
  - Requires sku (if inventory-backed), description, quantity, unit_price
  - line_total = quantity * unit_price
- labor
  - Requires description, labor_hours, hourly_rate
  - quantity may be represented as labor_hours
  - line_total = labor_hours * hourly_rate
- services
  - Requires description and line_total or quantity/unit_price equivalent
  - Should reference a configured Service Module definition when linked to a catalog offering
- sales
  - Supports standard sales transactions tracked on workorders
  - Requires description and line_total or quantity/unit_price equivalent

## Subtotal, Tax, Total
- subtotal = sum(all line_total values)
- tax_amount = subtotal * configured_tax_rate
- total = subtotal + tax_amount

## Rounding Policy
- Monetary values stored and computed using fixed precision decimal.
- Round tax_amount and total to 2 decimal places using standard half-up policy.

## Estimate and Final Invoice States
### MVP Minimum States
- draft_estimate
- approved_estimate
- finalized_invoice

## Billing Mode
- bill_now_receipt: complete sale with receipt generation at time of sale
- bill_later_invoice: record sale and generate invoice for later payment

### Rules
- Item edits are unrestricted while draft_estimate.
- After approved_estimate, material changes should require explicit re-approval flag.
- finalized_invoice locks item edits except admin override.

## Payment Status (MVP)
- unpaid
- partial
- paid

### Optional Payment Method Values
- cash
- card
- transfer
- other

### Optional Payment Method Fields
- check_number
  - Optional when payment method is transfer, other, or any check-based flow
- card_transaction_id
  - Optional external transaction reference captured from a third-party card processor/system

### Payment Field Validation
- check_number
  - Must be non-empty when provided
  - Should be unique per payment record when method indicates a check flow
- card_transaction_id
  - Must be non-empty when provided
  - Stores external processor reference only; no card PAN or CVV data is stored

## Tax Configuration
- One configured tax rate for MVP environment.
- Rate changes are versioned by effective date for auditability.

## Audit Requirements
- Record actor, timestamp, and before/after values for:
  - line item create/update/delete
  - estimate/invoice state changes
  - payment status updates

## Error Conditions
- Negative quantity, hourly_rate, or unit_price
- Invalid state transition for estimate/invoice state
- Tax configuration missing when total requested

## Validation Plan
- Deterministic billing test cases
- Tax rounding edge-case tests
- State transition tests for estimate/invoice lifecycle
- Authorization tests for locked invoice edits
- Optional payment field validation tests for check_number and card_transaction_id