# Workorders

Workorders is a container-first foundation for a work order management application.

Current release: `0.1.0`

Owner: Daniel Smith
GitHub: [Crashtechie](https://github.com/Crashtechie)

## Project Status

Version `0.1.0` is an initial platform release focused on infrastructure and health checks:

- Backend service running with FastAPI.
- Frontend served by Nginx using a multi-stage Node to Nginx Docker build.
- Docker health checks configured for backend and frontend containers.
- Repository-level and service-level `.dockerignore` and `.gitignore` hygiene in place.

## Architecture

The repository is split into two deployable services:

- `backend/`: Python FastAPI service exposing `GET /health` on port `8080`.
- `frontend/`: Nginx static web service exposing a health endpoint at `GET /healthz` on port `80`.

Frontend build behavior:

- If a React app (`package.json`) exists, Docker builds production assets with Node and serves them through Nginx.
- If prebuilt assets exist (`build/` or `dist/`), those are served.
- If neither exists, a safe placeholder page is generated so the container remains operational.

## Repository Structure

```text
Workorders/
  backend/
    Dockerfile
    main.py
    pyproject.toml
    requirements.txt
  docs/
    README.md
  frontend/
    Dockerfile
    nginx.conf
  CHANGELOG.md
  README.md
```

## Documentation

Project documentation is organized under the `docs/` directory.

- Start here: `docs/README.md`
- Backend service details: `backend/README.md`
- Frontend service details: `frontend/README.md`
- Repository baseline for release `0.1.0`: `docs/wiki/shared/repository-baseline-0.1.0.md`
- Includes issue tracking docs, logs, planning notes, templates, and wiki content split by backend, frontend, and shared scope.

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Frontend runtime: Nginx (Alpine)
- Frontend build stage: Node.js 20 (Alpine)
- Container tooling: Docker Buildx

## Run With Docker

From the repository root, use one terminal per service or run the commands sequentially.

### 1. Build backend image

```powershell
Set-Location backend
docker buildx build --no-cache -t workorders-backend:0.1.0 .
```

### 2. Run backend container

```powershell
docker run --rm -p 8080:8080 workorders-backend:0.1.0
```

Backend health check URL:

```text
http://127.0.0.1:8080/health
```

### 3. Build frontend image

```powershell
Set-Location ..\frontend
docker buildx build --no-cache -t workorders-frontend:0.1.0 .
```

### 4. Run frontend container

```powershell
docker run --rm -p 8081:80 workorders-frontend:0.1.0
```

Frontend health check URL:

```text
http://127.0.0.1:8081/healthz
```

## API Endpoints (Current)

- Backend: `GET /health` returns JSON service status.
- Frontend: `GET /healthz` returns a static health page for container health monitoring.

## Versioning and Change Log

This project follows Semantic Versioning.

- Current version: `0.1.0`
- Change history: see `CHANGELOG.md`

## Licensing

This project uses the GNU Affero General Public License v3.0 (AGPL-3.0).

License files are available at `LICENSE` and `COPYING` in the repository root.

## Roadmap (Planned)

- Implement complete work order domain models and CRUD APIs.
- Add authentication and role-based authorization.
- Add persistent data storage and migrations.
- Add frontend React UI for work order workflows.
- Add automated tests and CI/CD pipeline.
