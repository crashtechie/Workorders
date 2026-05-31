# Security, Audit, and Backup Baseline

## Purpose
Establish MVP security controls and operational safeguards required by planning decisions.

## Security Principles
- least privilege by role and action
- secure-by-default endpoint access
- no plaintext persistence for credential-like device data
- traceable sensitive operations through audit events

## Authentication and Authorization
- authenticated access required for all non-login endpoints
- role checks must be enforced at endpoint and object-action layers
- forbidden actions return role-consistent `403` responses

## Sensitive Data Handling
- device credential content must not be stored in plaintext password fields
- if temporary credential notes are used, they must be restricted by role and protected in storage
- do not accept or store payment card PAN/CVV
- optional metadata (`card_transaction_id`, `check_number`) is reference-only

## Audit Event Requirements
Mandatory audit logging for:
- authentication events
- role-restricted actions
- workorder status transitions
- billing line changes and invoice state changes
- inventory stock events
- admin overrides

Audit payload baseline:
- actor identity
- action type
- target resource
- timestamp
- before/after snapshots where applicable
- trace id for request correlation

## Logging and Observability
- include structured logs for API errors and business rule rejections
- avoid logging sensitive field values
- propagate trace ids through request lifecycle and error envelopes

## Backup and Recovery
- daily backups of persistent data
- documented point-in-time restore procedure
- restore drill included in release readiness

Operational readiness checks:
- backup job monitoring
- restore verification evidence
- retention policy validation

## Security Validation Checklist
- endpoint auth checks tested
- role matrix tests passed
- sensitive data non-plaintext policy verified
- audit event creation verified for all sensitive flows
- backup and restore drill evidence recorded
