# Backend Service

Version: `0.1.0`

This service provides the backend container baseline for Workorders. In version `0.1.0`, it exposes a single FastAPI health endpoint and is intended to validate the backend runtime, image build, and container health behavior.

## Current Behavior

- Framework: FastAPI
- App entrypoint: `main.py`
- Container runtime command: `python main.py`
- Listening port: `8080`
- Health endpoint: `GET /health`

Current response body:

```json
{"status":"healthy"}
```

## Local Container Workflow

Build the image from the `backend/` directory:

```powershell
docker buildx build --no-cache -t workorders-backend:0.1.0 .
```

Run the container:

```powershell
docker run --rm -p 8080:8080 workorders-backend:0.1.0
```

Verify the health endpoint:

```text
http://127.0.0.1:8080/health
```

## Key Files

- `main.py`: FastAPI app and `/health` route.
- `requirements.txt`: runtime Python dependencies.
- `pyproject.toml`: project metadata with version `0.1.0`.
- `Dockerfile`: container build and health check definition.

## Scope For 0.1.0

This release is an infrastructure baseline only. It does not yet include business APIs, persistence, authentication, or domain models.
