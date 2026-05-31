# ADR-002: Authorization Model

**Date:** 2026-05-28  
**Status:** Accepted  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** The Workorders system must restrict access to sensitive operations (user management, inventory administration, billing) based on each staff member's business role, while allowing shared access to common operations like creating and viewing workorders.
- **Driving factors:** Business roles map directly to operational responsibilities; unauthorized changes to billing, inventory, or user accounts represent significant business risk.
- **Deadline:** Must be established before any endpoint or UI implementation to prevent retrofitting permissions.
- **Affected components:** Backend API endpoints, frontend route and component visibility, and the user/session model.

---

## Considered Options

### Option 1: Role-Based Access Control (RBAC) with Named Business Roles

**Description:** Each user is assigned one of three roles — `sales_staff`, `technician`, or `admin`. Every protected API endpoint and UI element checks the caller's role against a defined permission matrix.

**Pros:**
- Maps directly to how the business organizes staff responsibilities
- Simple to reason about and audit: one role per user, fixed permission sets
- Easy to enforce at the API middleware layer (JWT claims or session role field)
- Role matrix can be documented and tested independently

**Cons:**
- Coarse-grained; cannot express "this technician can only edit their own workorders" without additional ownership checks
- Adding a new role in the future requires matrix and code updates

### Option 2: Attribute-Based Access Control (ABAC)

**Description:** Access decisions are made based on combinations of user attributes, resource attributes, and environmental conditions (e.g., "the requesting user owns this workorder AND it is in draft status").

**Pros:**
- Highly flexible and expressive
- Supports fine-grained ownership and contextual rules

**Cons:**
- Significantly more complex to implement, test, and reason about
- Over-engineered for an MVP with three clearly defined roles
- Harder to audit ("why was this user denied?")

### Option 3: Permission Flags per User (ACL)

**Description:** Each user account has a set of individual permission flags (e.g., `can_manage_inventory`, `can_view_reports`) that are configured per-user.

**Pros:**
- Maximum flexibility for one-off permission grants

**Cons:**
- Eliminates the predictability of role-based rules
- Harder to onboard new staff consistently
- Admin burden increases with every new permission requirement

---

## Decision Outcome

> **Decided:** We will implement **role-based access control (RBAC)** with three named roles: `sales_staff`, `technician`, and `admin`. Roles are assigned by an administrator and enforced at every protected API endpoint and reflected in frontend UI visibility.

---

## Rationale

1. **Best fit for requirements:** The three roles map directly to the three operational profiles defined in the project scope (intake/sales, technical work, administration).
2. **Long-term scalability:** A documented role matrix is straightforward to extend if a fourth role is needed post-MVP.
3. **Team expertise:** RBAC is well-understood and has clear implementation patterns in Django/DRF (`IsAuthenticated` + custom permission classes for role checks) and React (context-driven conditional rendering).
4. **Maintenance & support:** Simple to audit — a permission matrix document enumerates every endpoint/action and required role.
5. **Integration:** Role is encoded in the JWT/session token so the frontend and backend both enforce it independently.
6. **Risk mitigation:** Eliminates the risk of a sales staff member modifying inventory or billing configurations outside their role.

---

## Implementation Notes

- **First steps:** Define the role permission matrix as a shared artifact; implement a custom DRF `BasePermission` class per role; configure `DEFAULT_PERMISSION_CLASSES` in DRF settings; add a role-aware auth context in the React app.
- **Dependencies:** ADR-001 (Application Architecture) for where enforcement happens; JWT/session strategy must be finalized.
- **Success criteria:** No role-restricted endpoint is reachable without the correct role; frontend hides or disables controls not applicable to the current user's role.
- **Migration path:** N/A — greenfield project.

---

## Consequences

### Positive Consequences
- Predictable, auditable access control that matches business operations
- Role checks can be unit-tested independently of business logic
- Reduces risk of accidental privilege escalation

### Negative Consequences / Trade-offs
- Does not support resource-level ownership rules in MVP (e.g., "only the assigned technician can edit this workorder") — deferred as a post-MVP enhancement if required
- Role changes require an admin action; no self-service role upgrade path
