# Backend Logs

This folder contains backend-specific diagnostic logs.

## Typical Contents

- Backend Docker build failures
- Backend runtime startup errors
- API server stack traces

## Current Examples In This Folder

- `docker-build-errors_20260527_190522.log`
- `mainpy-run-errors_20260527_1805SS.log`

## Usage Notes

- Add new logs with timestamped names.
- Keep logs focused on one command/session per file when possible.
- Redact sensitive values before commit.
