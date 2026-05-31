# Backend Service

Version: `0.1.0`

This service provides the backend container baseline for Workorders. The current implementation is a Django bootstrap with a minimal health endpoint and project scaffold intended to validate runtime, image build, and container health behavior before full API/domain implementation.

## Current Behavior

- Framework: Django
- Bootstrap entrypoint: `main.py`
- Container runtime command: `python main.py`
- Listening port: `8080`
- Health endpoint: `GET /health`
- Django administrative entrypoint: `manage.py`
- Django project package: `config/`

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

Optional local scaffold command flow (without Docker):

```powershell
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
```

## Key Files

- `main.py`: minimal Django health-check stub used by container runtime.
- `manage.py`: Django administrative command entrypoint.
- `config/settings.py`: Django project settings scaffold.
- `config/urls.py`: URL routing scaffold.
- `requirements.txt`: runtime Python dependencies (Django/DRF stack).
- `pyproject.toml`: project metadata with version `0.1.0`.
- `Dockerfile`: container build and health check definition.

## Scope For 0.1.0

This release baseline does not yet include implemented business APIs, persistence integration, authentication wiring, or completed domain models.
