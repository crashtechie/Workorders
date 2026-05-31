# ADR-007: Integration Strategy

**Date:** 2026-05-28  
**Status:** Accepted  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** Small businesses typically use external tools for payments (Square, Stripe), accounting (QuickBooks), and customer relationship management. The Workorders system will eventually need to interoperate with some of these. The question is whether to build those integrations in the MVP or defer them.
- **Driving factors:** External integrations introduce third-party dependencies, authentication complexity, webhook infrastructure, and ongoing maintenance obligations. The MVP's primary goal is to establish correct core operations — integrations add risk without delivering the core value.
- **Deadline:** Must be decided before API and data model work begins to determine whether integration extension points need to be scaffolded in MVP.
- **Affected components:** Backend API design, payment workflows, billing data model, and any outbound notification or sync infrastructure.

---

## Considered Options

### Option 1: Defer All External Integrations — Build Integration-Ready Extension Points

**Description:** No live integrations with payment gateways, CRM tools, or accounting APIs are implemented in MVP. The backend API and data model are designed with integration-readiness in mind (clean entity IDs, consistent event patterns, no hardcoded assumptions that block future integration) but no active connectors are built.

**Pros:**
- Eliminates third-party dependency risk from MVP scope
- Keeps initial release focused on core operational correctness
- Allows integration requirements to be validated against real usage before building
- Integration-ready design costs little and avoids painful retrofitting

**Cons:**
- Payments must be handled outside the system (cash, separate terminal) in MVP
- No automated accounting sync means manual data transfer for bookkeeping in MVP

### Option 2: Implement Payment Gateway Integration in MVP

**Description:** Integrate with a payment processor (e.g., Stripe) to record payments and process transactions from within the workorder billing workflow.

**Pros:**
- End-to-end billing workflow in a single system from day one

**Cons:**
- Payment gateway integration requires PCI-DSS scope assessment
- Webhook infrastructure, refund handling, and failure recovery add significant complexity
- Third-party API dependency in MVP — an outage in the payment provider affects core operations
- Explicitly out of scope per project-scope-mvp.md

### Option 3: Implement Accounting API Integration in MVP

**Description:** Sync workorder billing data to an accounting tool (e.g., QuickBooks) in real time.

**Pros:**
- Eliminates manual bookkeeping data entry

**Cons:**
- OAuth and API credential management for a third-party system adds security surface
- Data mapping between workorder line items and chart-of-accounts entries is non-trivial
- Integration bugs in accounting data can have real financial consequences
- Deferred per project-scope-mvp.md

---

## Decision Outcome

> **Decided:** We will **defer all external integrations** (payment gateways, CRM, accounting APIs) until post-MVP. The MVP backend will be designed with integration-ready extension points: clean entity IDs suitable for external reference, a consistent REST API structure, and no hardcoded assumptions that would block adding connectors later.

---

## Rationale

1. **Best fit for requirements:** The project scope explicitly marks payment gateway and external API integrations as out of scope for MVP; this ADR formalizes that boundary.
2. **Long-term scalability:** Designing the API with clean entity IDs and RESTful conventions creates a natural integration surface for Phase 3 without rework.
3. **Team expertise:** Delaying integrations allows the team to focus on domain correctness first; integration patterns can be evaluated against real workorder data in Phase 3.
4. **Maintenance & support:** Fewer active dependencies in MVP means fewer failure modes and simpler operations.
5. **Integration:** Extension points will be documented as part of the API spec so Phase 3 integration work can proceed without reverse-engineering the core model.
6. **Risk mitigation:** Removing payment and accounting scope eliminates PCI-DSS surface and third-party API failure risks from the MVP.

---

## Implementation Notes

- **First steps:** Document integration extension points in the API spec (e.g., workorder IDs are stable external references; billing totals are exposed via a dedicated endpoint); allow only integration-neutral payment reference metadata in MVP billing (for example, `check_number` and external `card_transaction_id`) while still avoiding live gateway coupling.
- **Dependencies:** ADR-001 (Application Architecture) for the REST API foundation; ADR-003 (Domain Model) to ensure entity IDs and event timestamps are integration-ready.
- **Success criteria:** MVP ships with no active third-party integration dependencies; the API spec includes a documented integration extension point section that Phase 3 can use as a starting point.
- **Migration path:** Phase 3 integration work will add new API routes and webhook infrastructure without modifying core workorder and billing endpoints.

---

## Consequences

### Positive Consequences
- MVP scope is protected from third-party dependency and compliance risk
- Integration requirements can be validated against real operational data before building
- Clean API design now avoids costly retrofitting in Phase 3

### Negative Consequences / Trade-offs
- Payments must be processed outside the system in MVP; staff must reconcile manually
- No automated accounting sync means bookkeeping involves a manual export-and-import step
- Phase 3 integration work is a committed roadmap item that must be resourced after MVP launch
