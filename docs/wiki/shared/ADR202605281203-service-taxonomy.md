# ADR-004: Service Taxonomy

**Date:** 2026-05-28  
**Status:** Accepted  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** Workorders need to be classified by service type (e.g., "Screen Repair", "Data Recovery", "Device Sale") so that staff can categorize work consistently, reporting is meaningful, and billing line items are attributed correctly. The business must be able to define and maintain its own service catalog without requiring code changes.
- **Driving factors:** Services offered by a repair shop change over time; hard-coding service names would require developer intervention for routine business administration. Service location (on-site vs. in-shop) is an independent dimension and must not be conflated with service type.
- **Deadline:** Must be decided before workorder and billing data models are finalized.
- **Affected components:** `service_definition` entity, workorder creation/edit forms, billing line items, reporting filters, and admin configuration UI.

---

## Considered Options

### Option 1: Configurable Service Module (Business-Managed Catalog)

**Description:** A dedicated `service_definition` entity stores service names, descriptions, pricing hints, and active/inactive status. Administrators manage the catalog through the application UI. Workorders reference a `service_definition` by foreign key. `service_location` is captured as a separate field on the workorder.

**Pros:**
- Business can add, edit, activate, or deactivate services without any code or deployment change
- Service names and descriptions are consistent across all workorders and reports
- Inactive services remain referenceable on historical workorders (data integrity)
- Clean separation of "what kind of work" (service type) from "where it was done" (service location)

**Cons:**
- Requires a service-definition CRUD admin UI and API
- Workorder creation must validate that the selected service_definition is active
- Referential integrity constraint means deleting a service used by past workorders requires soft-delete (deactivation) rather than hard-delete

### Option 2: Hardcoded Enum of Service Types in Code

**Description:** Service types are an enum value in the codebase (e.g., `SCREEN_REPAIR`, `DATA_RECOVERY`). New services require a code change, migration, and redeployment.

**Pros:**
- Zero admin UI needed
- Simple schema — no service_definition table

**Cons:**
- Every new or removed service requires a developer and a deployment
- Violates the business requirement that services be business-managed
- Explicitly rejected in project-scope-mvp.md resolved decisions

### Option 3: Free-Text Service Description on Workorder

**Description:** Staff type a free-text service description on each workorder with no controlled vocabulary.

**Pros:**
- Maximum flexibility, no admin setup required

**Cons:**
- Destroys reporting consistency (same service spelled ten different ways)
- No basis for aggregation or filtering by service type
- Incompatible with billing and reporting requirements

---

## Decision Outcome

> **Decided:** We will implement a **configurable Service Module** where service definitions are business-managed data records. Administrators can add, edit, activate, and deactivate services through the application. Workorders reference an active `service_definition` by foreign key. `service_location` is a separate, independently captured field on the workorder.

---

## Rationale

1. **Best fit for requirements:** The business explicitly requires the ability to configure services without code changes; this is a resolved decision in the project scope.
2. **Long-term scalability:** The catalog can grow to any number of services without touching the codebase.
3. **Team expertise:** A standard CRUD admin module for reference data is straightforward to implement with Django Admin (for admin-role management) and DRF viewsets (for API access).
4. **Maintenance & support:** Active/inactive status supports safe service retirement without data loss.
5. **Integration:** A structured service catalog is required for any future reporting, analytics, or accounting integration that needs consistent categorization.
6. **Risk mitigation:** Referential validation at workorder creation prevents stale or invalid service references; deactivation rather than deletion protects historical record integrity.

---

## Implementation Notes

- **First steps:** Define the `service_definition` schema (id, name, description, is_active, created_at, updated_at); implement admin CRUD endpoints; add `service_definition_id` foreign key on the workorder entity.
- **Dependencies:** ADR-003 (Domain Model) for entity placement; ADR-002 (Authorization Model) for role controls — only `admin` may manage service definitions.
- **Success criteria:** Admin can add a new service type and it is immediately available for selection on new workorders; deactivated services no longer appear in the workorder creation form but remain visible on historical records.
- **Migration path:** N/A — greenfield project. Initial service catalog is populated by the business during onboarding.

---

## Consequences

### Positive Consequences
- Business operations team is self-sufficient for service catalog management
- Reports and filters on service type are consistent and meaningful
- Historical workorders are never broken by service catalog changes

### Negative Consequences / Trade-offs
- Service-definition CRUD adds scope to the admin module
- Workorder creation must enforce active-service validation
- Hard-delete of service definitions is blocked by referential integrity — deactivation is the only safe removal path
