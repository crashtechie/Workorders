# Inventory and Stock Events

## Purpose
Define the MVP inventory behavior for stock accounting, workorder linkage, low-stock reporting, and integrity controls.

## Inventory Scope
- inventory item CRUD
- stock movement events
- workorder-linked consumption
- low-stock threshold support

## Stock Event Types
- `purchase`: increase stock
- `consume`: decrease stock
- `adjust`: manual correction up or down

## Event Payload
Required:
- `inventory_item_id`
- `event_type`
- `quantity_delta`
- `reason`
- `actor_user_id`

Optional:
- `workorder_id` (required by policy for workorder-linked consume events)
- `note`

## Integrity Rules
- every stock change must write one stock event
- consume events must not reduce stock below allowed minimum unless admin override is used
- consume events linked to workorders should reference corresponding billing line/item when applicable
- reversal is modeled as an `adjust` event with explicit reason

## SKU and Catalog Rules
- SKU is unique and immutable after creation in MVP
- description and pricing metadata may be edited
- inactive flag is preferred over hard delete for historical references

## Low-Stock Logic
- low-stock threshold applies when `stock_on_hand <= reorder_point`
- `reorder_point` and `reorder_quantity` are optional in MVP
- low-stock indicators feed report/dashboard endpoints

## Workorder Integration Policy
- parts may be staged on workorder before confirmed consumption
- stock should decrement only at confirmed usage step
- if workorder edits remove consumed item effects, create balancing adjustment event

## Concurrency and Transactions
- stock mutation and event creation must occur in one DB transaction
- use conflict detection to prevent race-condition driven negative stock
- reject stale updates and return conflict response for retry path

## Validation and Tests
- each event type mutation tests
- transaction rollback tests for partial failure scenarios
- workorder-linked consumption validation tests
- low-stock threshold tests
- actor/reason mandatory enforcement tests
