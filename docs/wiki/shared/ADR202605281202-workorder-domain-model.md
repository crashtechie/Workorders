# ADR-003: Workorder Domain Model

**Date:** 2026-05-28  
**Status:** Accepted  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** The core data model must accurately represent the business objects of a computer repair and sales shop — customers, workorders, the items billed on each workorder, inventory parts, and the stock movements that link them — in a way that supports searchability, itemized billing, and traceable inventory consumption.
- **Driving factors:** Billing correctness, inventory accuracy, and the ability to look up historical workorders and audit stock events are non-negotiable operational requirements.
- **Deadline:** Domain model must be finalized before backend schema and API work begins.
- **Affected components:** Backend data model, API shape, frontend forms, and reporting queries.

---

## Considered Options

### Option 1: Fully Normalized Separate Entities

**Description:** Define discrete entities — `customer`, `workorder`, `workorder_item`, `inventory_item`, and `stock_event` — each with their own table and explicit foreign-key relationships.

**Pros:**
- Supports independent querying of each entity (e.g., "all workorders for a customer", "all stock events for a part")
- Itemized billing is a first-class concern: each line item is a row with its own price, quantity, and type
- Inventory traceability: every consumption or adjustment is a stock event with actor, reason, and timestamp
- Extensible: new item types (e.g., a fee, a discount) can be added as new workorder_item subtypes

**Cons:**
- More tables to design and migrate
- Join complexity in queries; must be managed with care to avoid N+1 problems

### Option 2: Embedded Line Items as JSON in Workorder

**Description:** Store billing line items as a JSON array column directly on the workorder row.

**Pros:**
- Simpler schema — fewer tables
- Fast reads for the workorder detail view

**Cons:**
- Cannot independently query or report on line items (e.g., "total labor billed this month")
- No foreign-key integrity to inventory items
- Impossible to trace stock consumption from the inventory side
- Incompatible with the itemized billing and inventory traceability requirements

### Option 3: Flat Denormalized Workorder Table

**Description:** A single wide table captures all workorder data including customer info, device, billing total, and a notes field for line items.

**Pros:**
- Simplest possible schema

**Cons:**
- Breaks any ability to search by customer, report by item type, or track inventory
- Fundamentally incompatible with the MVP scope — ruled out immediately

---

## Decision Outcome

> **Decided:** We will use **fully normalized separate entities**: `customer`, `workorder`, `workorder_item`, `inventory_item`, and `stock_event`, with explicit foreign-key relationships and transactional consistency enforced at the backend layer.

---

## Rationale

1. **Best fit for requirements:** Separate entities directly model the business concepts the shop operates with; every MVP requirement maps cleanly to one or more entities.
2. **Long-term scalability:** Normalized entities support future reporting, analytics, and integrations without schema changes.
3. **Team expertise:** Relational modeling with PostgreSQL is well-understood; Django ORM supports this pattern directly with model classes, ForeignKey relations, and `select_related`/`prefetch_related` for query optimization.
4. **Maintenance & support:** Standard relational patterns are easy to reason about, test, and maintain.
5. **Integration:** A normalized model is required for any future accounting or CRM integration (post-MVP) to consume meaningful data.
6. **Risk mitigation:** Transactional consistency (e.g., stock decrement + stock_event creation in one transaction) prevents inventory drift; foreign keys prevent orphaned billing records.

---

## Implementation Notes

- **First steps:** Produce the full entity-relationship diagram and schema as part of `backend-data-model.md`; implement Django models and run `makemigrations`/`migrate` to manage schema.
- **Dependencies:** ADR-004 (Service Taxonomy) informs how service definitions relate to workorder_item; ADR-005 (Sensitive Data Handling) informs which fields on `workorder` require special treatment.
- **Success criteria:** All billing totals are reproducible by summing workorder_item rows; all stock adjustments are traceable via stock_event audit trail.
- **Migration path:** N/A — greenfield project.

---

## Consequences

### Positive Consequences
- Itemized billing reports and per-line queries are straightforward SQL
- Inventory accuracy is maintained by transactional stock_event records
- Customer search and workorder lookup are fully indexable
- Audit trail for billing and inventory is a natural outcome of the model

### Negative Consequences / Trade-offs
- Join-heavy queries require explicit optimization (indexed foreign keys, select_related patterns)
- Schema migrations must be managed carefully as the model evolves
- Transactional integrity must be enforced in the backend service layer — cannot be left to the client
