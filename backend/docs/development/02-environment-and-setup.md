# Backend Environment and Setup

## Purpose
Define a consistent local development baseline and implementation workflow for backend contributors.

## Runtime and Framework Baseline
Current repository baseline indicates:
- Python backend service under `backend/`
- Django and Django REST Framework dependencies declared in `pyproject.toml`
- container baseline and health probe behavior documented in `backend/README.md`

Implementation target for MVP API work:
- Django + DRF service architecture
- versioned REST endpoints under `/api/v1/...`

## Local Prerequisites
- Python 3.14 or newer
- virtual environment support
- PostgreSQL (or equivalent relational DB configured for local dev)
- Docker (optional, for containerized run and health checks)

## Local Setup Steps
1. Create and activate virtual environment.
2. Install runtime dependencies from `requirements.txt` and/or lock-managed environment.
3. Configure environment variables for local DB, auth secrets, and app settings.
4. Run database migrations.
5. Start backend development server.

## Recommended Environment Variables
- `APP_ENV=development`
- `DATABASE_URL=<local database connection>`
- `JWT_SECRET_KEY=<local dev secret>`
- `TAX_RATE_DEFAULT=<decimal value, example 0.0825>`
- `AUDIT_LOG_ENABLED=true`

## Suggested Project Layout (Implementation Target)
- `backend/config/`: Django project settings and URL configuration
- `backend/apps/auth/`: auth and role enforcement
- `backend/apps/customers/`: customer domain
- `backend/apps/workorders/`: workorder, device, service definitions
- `backend/apps/billing/`: workorder items, summaries, invoice states, payment metadata
- `backend/apps/inventory/`: inventory items and stock events
- `backend/apps/reports/`: report queries and CSV export
- `backend/apps/audit/`: audit event capture and query support

## Developer Workflow
1. Confirm requirement and ADR impact before coding.
2. Update serializer/model/validation tests first (or in same change).
3. Implement endpoint with role restrictions.
4. Verify audit event generation for sensitive actions.
5. Update traceability evidence in development docs.

## Container Workflow
Use the existing backend Docker instructions for image build/run validation and health checks. Treat container success as runtime smoke verification, not feature completeness.

## Definition of Ready for New Endpoint Work
- requirement ID mapped
- request/response contract specified
- role access matrix defined
- validation rules documented
- audit requirements identified
