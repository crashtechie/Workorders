# Repository Baseline 0.1.0

This document records the repository baseline for version `0.1.0` and serves as the reference point for the first commit in the Git history.

## Release Scope

Version `0.1.0` establishes the initial container-ready application skeleton:

- Backend FastAPI service with `GET /health`.
- Frontend Nginx service with `GET /healthz`.
- Multi-stage frontend container build.
- Repository and service ignore files for generated artifacts.
- Root and service README coverage for current runtime behavior.

## Documentation Baseline

The following files should stay aligned for the initial release:

- `README.md`
- `CHANGELOG.md`
- `backend/README.md`
- `frontend/README.md`
- `backend/pyproject.toml`

Current version recorded across the release baseline: `0.1.0`.

## Initial Commit Checklist

- Confirm the working tree only contains files intended for source control.
- Exclude generated build logs, virtual environments, build outputs, and local secrets through `.gitignore`.
- Ensure Docker image tags in documentation use `0.1.0` where the release version is referenced.
- Keep the first commit limited to the repository baseline, not future feature work.

## Recommended Initial Commit Scope

The initial commit should capture:

- backend container baseline
- frontend container baseline
- repository documentation
- licenses and changelog
- ignore rules required for clean local development

## Follow-On Work

Changes after the initial commit should be tracked as separate feature, fix, or documentation commits so the repository history has a clean baseline.
