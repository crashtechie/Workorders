# Frontend Service

Version: `0.1.0`

This service provides the frontend container baseline for Workorders. In version `0.1.0`, it serves static assets through Nginx and exposes a dedicated health endpoint for container monitoring.

## Current Behavior

- Runtime server: Nginx
- Public container port: `80`
- Health endpoint: `GET /healthz`
- Main route behavior: serve static assets from `/usr/share/nginx/html`

The Docker build currently supports three frontend states:

- If `package.json` exists, it installs dependencies and runs a production frontend build.
- If prebuilt `build/` or `dist/` assets exist, it serves those files directly.
- If neither source nor built assets exist, it generates a placeholder page so the container stays operational.

## Local Container Workflow

Build the image from the `frontend/` directory:

```powershell
docker buildx build --no-cache -t workorders-frontend:0.1.0 .
```

Run the container:

```powershell
docker run --rm -p 8081:80 workorders-frontend:0.1.0
```

Verify the health endpoint:

```text
http://127.0.0.1:8081/healthz
```

## Key Files

- `Dockerfile`: multi-stage Node to Nginx image build.
- `nginx.conf`: static asset routing and `/healthz` mapping.

## Scope For 0.1.0

This release provides frontend hosting infrastructure only. It does not yet include the production Workorders user interface.
