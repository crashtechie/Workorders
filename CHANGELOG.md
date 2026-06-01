# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]

### Added

- Django project scaffold under `backend/config/` with `manage.py` for administrative commands.
- Backend development documentation set under `backend/docs/development/`.
- Planning documentation for backend, frontend, and shared architecture under `docs/Planning/`.
- Shared ADR/wiki entries under `docs/wiki/shared/` for architecture, authorization, domain, taxonomy, and integration decisions.

### Changed

- Backend runtime baseline moved from FastAPI health endpoint implementation to a Django-based health check stub in `backend/main.py`.
- Backend Python dependencies now align to Django/DRF stack (`django`, `djangorestframework`, `psycopg2-binary`, `djangorestframework-simplejwt`) with lockfile updates.
- Docker compose backend service command and exposed ports were updated to support current backend development flow.
- Backend API paths were normalized to a versioned convention using `api/v1/<app>/` for application endpoints.
- JWT refresh endpoint moved to the versioned auth route `api/v1/auth/token/refresh/`.

### Fixed

- `config.tests` authentication and DRF default tests were updated to use versioned API routes.
- Config test setup now validates current Django test-run behavior for `DEBUG` handling.

## [0.1.0] - 2026-05-27

### Added

- Initial backend and frontend containerization setup.
- Frontend multi-stage Node to Nginx Docker build flow.
- Frontend health check endpoint at /healthz and container health check.
- Root, backend, and frontend Docker ignore hygiene improvements.
- Service-level backend and frontend README documentation.
- Shared repository baseline documentation for the initial release and first commit.
