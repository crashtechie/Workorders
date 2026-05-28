# Documentation Guide

This directory is the central home for project documentation that is not source code.

## Purpose

- Keep operational knowledge, planning notes, issue tracking, and long-form wiki content organized.
- Separate documentation by scope: backend, frontend, and shared.

## Directory Layout

- `issues/`: tracked defects, tasks, and follow-ups.
- `logs/`: captured command/runtime logs and troubleshooting output.
- `Planning/`: roadmap, implementation planning, and design proposals.
- `templates/`: reusable templates for docs in other folders.
- `wiki/`: reference knowledge and persistent project documentation.

## Conventions

- Use clear, descriptive filenames.
- Prefer dated filenames for time-based records, for example `2026-05-27-backend-healthcheck-issue.md`.
- Keep service-specific docs in `backend/` or `frontend/` subfolders.
- Put cross-service material in `shared/`.

## Relationship To Source Code

- Code lives in project service directories such as `backend/` and `frontend/`.
- This `docs/` tree explains and supports that code, but should not contain executable app logic.
