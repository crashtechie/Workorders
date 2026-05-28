# Logs Documentation

This folder stores captured command output and runtime logs used for debugging.

## Purpose

- Preserve troubleshooting evidence.
- Keep logs grouped by service scope.

## Subdirectories

- `backend/`: backend build/run logs.
- `frontend/`: frontend build/run logs.
- `shared/`: cross-service or repository-level logs.

## Logging Practices

- Prefer timestamped filenames.
- Keep only useful logs; remove stale noise regularly.
- Do not commit secrets, credentials, or private tokens in log files.

## Suggested Naming

- `docker-build-errors_YYYYMMDD_HHMMSS.log`
- `run-errors_YYYYMMDD_HHMMSS.log`
