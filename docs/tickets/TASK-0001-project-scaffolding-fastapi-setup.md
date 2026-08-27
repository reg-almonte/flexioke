---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0001: Project Scaffolding, FastAPI Setup & Dependencies Configuration

## Parent Story
- `STORY-0001-backend-foundation-ingestion.md`

## What to build
Set up the Python project structure, requirements/dependencies configuration (`fastapi`, `uvicorn`, `audio-separator`, `yt-dlp`, `pydantic`, `python-multipart`, `pytest`, `httpx`), and the main FastAPI application entrypoint with CORS middleware and static asset mounting.

## Acceptance Criteria
- [x] Requirements and dependencies are declared and installable.
- [x] FastAPI application initializes cleanly with CORS and base error handling.
- [x] Root health-check endpoint `GET /api/health` returns operational status.
- [x] Static files directory is mounted and ready to serve frontend assets.

## Blocked by
- None (can start immediately)

## Implementation
- **Branch:** `story/STORY-0001-backend-foundation-ingestion`
- **Scaffolding:** `requirements.txt`, `src/main.py`, `src/api/routes.py`, `src/static/`, `tests/test_health.py`
- **Tests:** 2 unit tests passing (health endpoint & static SPA index serving).
