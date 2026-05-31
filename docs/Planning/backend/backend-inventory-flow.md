# Backend Inventory Flow (MVP)

## Objective
Define inventory behavior for stock tracking and consumption tied to workorders.

## Scope
- Inventory item CRUD
- Stock movement event logging
- Workorder-linked parts consumption
- Low-stock detection baseline

## Stock Event Types
- purchase: increases stock_on_hand
- consume: decreases stock_on_hand
- adjust: manual correction up/down with reason

## Event Payload Baseline
### Required Fields
- inventory_item_id
- event_type
- quantity_delta
- reason
- actor_user_id

### Optional Fields
- workorder_id (required for consume tied to workorder)
- note

## Rules
- consume must not reduce stock below allowed minimum threshold unless admin override is enabled.
- every stock_on_hand mutation must create a stock_event record.
- consume events linked to workorders should reference associated itemized billing line when applicable.

## SKU and Catalog Rules
- sku is unique and immutable after creation in MVP.
- inventory descriptions are editable.
- inactive flag can replace hard delete for historical integrity.

## Reorder Logic
- reorder_point and reorder_quantity are optional in MVP data model.
- Low-stock condition when stock_on_hand <= reorder_point (if reorder_point is set).
- Low-stock data appears in reports/dashboard; notifications can be post-MVP.

## Workorder Integration
- Parts added to a workorder can trigger stock allocation/consumption.
- Consumption occurs at confirmed usage step to avoid premature stock reduction.
- Reversal requires an adjust event with reference reason.

## Concurrency and Integrity
- Use transactional update for stock_on_hand and stock_event creation.
- Detect and reject conflicting updates where applicable.

## Validation Plan
- Stock mutation tests by event type
- Workorder-linked consumption tests
- Low-stock threshold tests
- Integrity tests for event/quantity consistency

## Risks and Mitigations
- Risk: negative stock from race conditions
  - Mitigation: transactional checks and conflict handling
- Risk: untraceable manual changes
  - Mitigation: mandatory reason and actor on adjustments