# ADR-005: Sensitive Data Handling

**Date:** 2026-05-28  
**Status:** Accepted  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** Repair shop workorders may involve temporary access to customer device credentials (login passwords, PINs, lock codes). If these are captured in the system, persistent plaintext storage creates an unnecessary and ongoing exposure risk — both to the business and to customers.
- **Driving factors:** Operational liability, customer trust, and data protection best practices. A breach of stored plaintext device passwords would be a serious harm to customers.
- **Deadline:** Must be decided before any data model or form implementation that involves device details.
- **Affected components:** The workorder entity's device detail fields, the backend storage layer, and any frontend forms that collect device credentials.

---

## Considered Options

### Option 1: Prohibit Persistent Plaintext Storage — Use Temporary Secure Note Pattern

**Description:** Device passwords and credentials are never stored in plaintext in the database. If a credential must be captured temporarily (e.g., for a technician to complete work), it is stored in an encrypted or restricted field with role-restricted visibility. The credential is not written to standard workorder records or logs.

**Pros:**
- Eliminates the primary exposure vector: a database read or backup dump cannot yield plaintext credentials
- Aligns with the principle of least privilege — only authorized roles can see sensitive fields
- Reduces regulatory and liability risk
- Customers are protected even if the database is compromised

**Cons:**
- More implementation complexity than a simple text column
- Staff workflow must be designed to not rely on the system as a permanent credential vault
- Requires clear UX communication so staff understand the field's purpose and limitations

### Option 2: Store Credentials in a Standard Encrypted Column

**Description:** Credentials are stored encrypted at rest using application-level encryption (e.g., AES-256 with a stored key), decrypted on demand.

**Pros:**
- Data is not plaintext at rest
- Still accessible if needed for audit or reference

**Cons:**
- Key management complexity: where is the encryption key stored? If co-located, it reduces the practical security benefit.
- Creates an indefinite record of customer credentials, increasing long-term exposure window
- Complicates backup and restore operations

### Option 3: Store Credentials as Plaintext in the Database

**Description:** A simple text column stores whatever the staff member enters.

**Pros:**
- Zero implementation complexity

**Cons:**
- Plaintext customer credentials in the database represent a severe security vulnerability
- Incompatible with the project scope's "zero plaintext storage of protected sensitive fields" success metric
- Immediately rejected on security grounds

---

## Decision Outcome

> **Decided:** We will **prohibit persistent plaintext storage of device passwords and credentials**. If a credential must be temporarily captured, it will use a restricted-visibility field pattern with role-based access controls. Credentials are never written to standard text logs, audit trails, or exportable reports.

---

## Rationale

1. **Best fit for requirements:** The project scope explicitly lists "zero plaintext storage of protected sensitive fields" as a success metric and a resolved decision.
2. **Long-term scalability:** Avoiding credential storage eliminates an entire class of future security incidents.
3. **Team expertise:** Role-restricted field patterns and audit exclusions are implementable with the chosen stack.
4. **Maintenance & support:** Fewer sensitive fields mean simpler security review and compliance posture.
5. **Integration:** Any future export or reporting feature will never need to handle credential sanitization if credentials are never in the standard data model.
6. **Risk mitigation:** This decision directly addresses the most likely source of customer harm from a data breach scenario.

---

## Implementation Notes

- **First steps:** Identify all workorder fields that could capture credentials; mark them as `sensitive: true` in the data model documentation; implement backend-level response filtering to exclude these fields from standard API responses unless the requesting role is authorized.
- **Dependencies:** ADR-002 (Authorization Model) for role-restricted visibility rules; ADR-003 (Domain Model) for field placement on the workorder entity.
- **Success criteria:** A database dump of the `workorder` table contains no plaintext customer credentials; the API does not return sensitive fields to unauthorized roles; credentials do not appear in CSV exports or audit logs.
- **Migration path:** N/A — greenfield project.

---

## Consequences

### Positive Consequences
- Customer credentials are not exposed in backups, exports, or logs
- Reduces liability in the event of a database breach
- Simplifies compliance with data protection obligations

### Negative Consequences / Trade-offs
- Staff must understand the temporary-note workflow and cannot use the system as a long-term credential vault
- Requires clear UI guidance on sensitive fields to prevent misuse
- Field-level access control adds backend implementation complexity for the restricted fields
