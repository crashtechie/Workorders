# ADR-008: Backend Framework Selection

**Date:** 2026-05-28  
**Status:** Accepted  
**Supersedes:** N/A  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** The Workorders MVP backend is a Python web service that must expose a REST API, enforce role-based access control, manage a relational data model with migrations, support an admin configuration interface for business-managed data (service catalog, user management), and produce auditable, testable business logic.
- **Driving factors:** The backend framework must support rapid development of CRUD operations, a built-in admin interface, ORM-backed migrations, and an authentication/authorization stack without assembling these from scratch.
- **Deadline:** Must be decided before any backend implementation begins; affects project structure, dependency selection, and developer workflow.
- **Affected components:** The entire backend service — API layer, data model, authentication, admin, migrations, and testing.

---

## Considered Options

### Option 1: Django with Django REST Framework (DRF)

**Description:** Django is a batteries-included Python web framework with a built-in ORM, migration system, admin interface, authentication backend, and session/cookie management. Django REST Framework extends it with serializers, viewsets, routers, and token/JWT authentication for API-first development.

**Pros:**
- Built-in ORM with a mature migration system (Alembic not required — Django manages migrations natively)
- Django Admin provides a fully functional, role-aware admin interface for business-managed data (service catalog, user accounts) with minimal additional code
- Django's authentication and permissions system is well-documented and directly maps to the RBAC requirements
- DRF provides serializers, viewset abstractions, and automatic router-based URL generation for REST APIs
- Large ecosystem: extensive third-party packages, long-term community support
- Integrated test client for API endpoint testing without a running server
- Django's ORM supports complex queries, annotations, and transactions needed for billing and inventory logic

**Cons:**
- More opinionated than FastAPI — project structure is largely prescribed
- Slightly more boilerplate for pure API projects compared to FastAPI's minimal decorator style
- Async support is available but requires care; Django's default request handling is synchronous

### Option 2: FastAPI with SQLAlchemy

**Description:** FastAPI is a modern, high-performance Python web framework based on Pydantic and ASGI. It pairs with SQLAlchemy for ORM and Alembic for migrations.

**Pros:**
- Automatic OpenAPI/Swagger documentation generation
- Native async support across the entire request lifecycle
- Type-driven validation via Pydantic models
- Lightweight — assemble only the pieces needed

**Cons:**
- No built-in admin interface — a business-managed service catalog and user management UI must be built entirely from scratch
- Authentication and RBAC must be assembled from separate packages (python-jose, passlib, custom dependencies)
- Migrations managed by Alembic, which requires separate configuration and is less integrated than Django's `makemigrations`/`migrate` workflow
- More assembly work for features Django provides out of the box (admin, auth, permissions)
- The team's needs are well-served by the batteries-included approach given the scope

### Option 3: Flask with SQLAlchemy

**Description:** Flask is a minimal Python web framework. REST API patterns and ORM integration require assembling multiple extensions (Flask-RESTful or Flask-RESTX, Flask-SQLAlchemy, Flask-Migrate, Flask-Login).

**Pros:**
- Very lightweight and flexible
- Familiar to many Python developers

**Cons:**
- Maximum assembly required — no admin, no ORM, no auth, no migrations out of the box
- Multiple third-party extensions must be maintained and kept compatible with each other
- Weakest option for the full scope of this project
- No meaningful advantage over Django or FastAPI for this use case

---

## Decision Outcome

> **Decided:** We will use **Django with Django REST Framework (DRF)** as the backend framework. Django's integrated ORM, migration system, admin interface, and authentication stack directly serve the Workorders MVP requirements with minimal assembly overhead.

---

## Rationale

1. **Best fit for requirements:** Django Admin covers the service catalog and user management administration requirements. DRF covers the REST API layer. Django's ORM covers the normalized data model. All are first-class, integrated Django features.
2. **Long-term scalability:** Django is a mature, stable framework with a long support lifecycle. The ORM and admin scale well beyond MVP scope.
3. **Team expertise:** Django is the agreed-upon framework for this project; the team will develop expertise on it directly.
4. **Maintenance & support:** Django has one of the largest Python web framework communities and a clear Long Term Support (LTS) release cycle.
5. **Integration:** DRF's serializers and viewsets align naturally with the API contracts defined in the architecture decisions; token or JWT authentication integrates cleanly.
6. **Risk mitigation:** Using an integrated stack reduces the risk of incompatible package versions or gaps in the assembled toolchain. The Django admin reduces the scope of custom admin UI work significantly.

---

## Implementation Notes

- **First steps:** Initialize a Django project (`django-admin startproject`); create a Django app per major domain area (e.g., `workorders`, `customers`, `inventory`, `services`); configure DRF in `settings.py`; set up PostgreSQL as the database backend.
- **Dependencies:** `django`, `djangorestframework`, `psycopg2-binary` (or `psycopg[binary]`), `djangorestframework-simplejwt` for JWT authentication.
- **Success criteria:** All MVP API endpoints are reachable via DRF viewsets; Django Admin provides the service catalog and user management interface; Django migrations manage all schema changes.
- **Migration path:** The placeholder `main.py` health check stub will be replaced by a proper Django project structure as backend development begins.

---

## Consequences

### Positive Consequences
- Django Admin eliminates the need to build a separate admin UI for service catalog and user management
- Integrated ORM + migrations reduce the toolchain surface
- DRF provides serializer validation that aligns with backend-owns-validation architecture principle
- Comprehensive test client for endpoint testing without infrastructure

### Negative Consequences / Trade-offs
- Django's synchronous-by-default model means async operations (if needed) require explicit `async` views and an ASGI server (e.g., `uvicorn` or `daphne`)
- The placeholder `main.py` FastAPI health check stub is superseded — the health endpoint will be provided by the Django application
- Django's opinionated project layout must be followed; deviating from conventions adds maintenance cost
