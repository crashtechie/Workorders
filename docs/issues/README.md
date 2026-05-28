# Issues Documentation

This folder tracks known problems, bugs, and action items.

## Purpose

- Capture issue context in writing so troubleshooting and fixes are reproducible.
- Separate issue records by service ownership.

## Subdirectories

- `backend/`: backend-specific defects and investigation notes.
- `frontend/`: frontend-specific defects and investigation notes.
- `shared/`: issues that involve both services, infrastructure, or repository-wide concerns.

## Suggested File Content

Each issue document should include:

- Summary and impact
- Reproduction steps
- Expected vs actual behavior
- Environment details
- Root cause (if known)
- Resolution and validation

## Naming Suggestion

Use date-first naming for easier sorting, for example:

- `2026-05-27-frontend-docker-build-failure.md`

