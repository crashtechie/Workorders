# Billing and Tax Implementation

## Purpose
Define deterministic billing behavior and implementation constraints for line items, totals, invoice states, and payment metadata.

## Supported Line Item Types
- `parts`
- `labor`
- `services`
- `sales`

## Line Calculation Rules

### Parts
Required:
- `description`
- `quantity`
- `unit_price`

Optional:
- `sku` when inventory-backed

Formula:
- `line_total = quantity * unit_price`

### Labor
Required:
- `description`
- `labor_hours`
- `hourly_rate`

Formula:
- `line_total = labor_hours * hourly_rate`

### Services and Sales
Required:
- `description`
- either explicit `line_total` or quantity/unit price equivalent

Service-related lines should reference configured service definitions when applicable.

## Totals
- `subtotal = sum(line_total)`
- `tax_amount = subtotal * configured_tax_rate`
- `total = subtotal + tax_amount`

## Rounding and Precision
- use fixed precision decimals for all monetary values
- round tax and total to 2 decimal places with half-up policy

## Billing State Model
Invoice/estimate states:
- `draft_estimate`
- `approved_estimate`
- `finalized_invoice`

State behavior:
- `draft_estimate`: item edits allowed
- `approved_estimate`: material changes require explicit re-approval marker
- `finalized_invoice`: item edits locked except admin override

## Billing Modes
- `bill_now_receipt`
- `bill_later_invoice`

## Payment Status and Metadata
Payment status values:
- `unpaid`
- `partial`
- `paid`

Payment methods (optional):
- `cash`
- `card`
- `transfer`
- `other`

Optional metadata:
- `check_number`
- `card_transaction_id`

Validation:
- both metadata fields must be non-empty if provided
- `check_number` should be unique per payment record in check-based flows
- no card PAN, CVV, or similar cardholder data may be accepted or persisted

## Tax Configuration
- one active tax rate for MVP scope
- tax rate changes must be versioned by effective date
- billing responses should include tax rate context used for calculation

## Audit Requirements
Emit audit entries with actor and timestamp for:
- line create/update/delete
- estimate/invoice state transitions
- payment status changes
- admin overrides on locked invoices

## Error Conditions
- negative quantity, unit price, labor hours, or hourly rate
- invalid billing state transition
- missing tax configuration during totalization request
- immutable finalized invoice edits without allowed override

## Test Matrix
- deterministic subtotal/tax/total scenarios
- rounding edge cases
- state transition restrictions
- partial payment flows
- metadata validation for check and card references
