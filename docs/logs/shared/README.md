# Shared Logs

Use this folder for logs that involve both services or repository-level operations.

## Includes

- Multi-service startup diagnostics
- CI/CD log captures
- Cross-cutting tooling output

## Excludes

- Service-specific logs that belong in `../backend/` or `../frontend/`

## Recommended Metadata In Log Headers

- Command executed
- Working directory
- Timestamp
- Exit code
