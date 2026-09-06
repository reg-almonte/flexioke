---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager

## Parent Story
- `STORY-0001-backend-foundation-ingestion.md`

## What to build
Implement the core Job model, filesystem directory manager (`./data/jobs/{job_id}/`), JSON metadata serializer/deserializer (`job.json`), status polling handler, and bounded background worker executor for serializing resource-heavy separation jobs.

## Acceptance Criteria
- [x] Unique UUID job directories are safely initialized.
- [x] Job state transitions (`queued`, `downloading`, `separating_stage_1`, `separating_stage_2`, `completed`, `failed`) serialize to disk atomically.
- [x] Status endpoint `GET /api/jobs/{job_id}` returns up-to-date status, progress percentage, stage description, and error details if applicable.
- [x] Unit tests cover job creation, serialization, updates, and concurrency limits.

## Blocked by
- TASK-0001: Project Scaffolding, FastAPI Setup & Dependencies Configuration

## Implementation
- **Branch:** `story/STORY-0001-backend-foundation-ingestion`
- **Models:** `src/models.py` (`JobStatus`, `SourceType`, `JobRecord` with Pydantic v2).
- **Service:** `src/services/job_manager.py` with thread-safe atomic disk persistence, cache loading, and bounded `ThreadPoolExecutor`.
- **API:** `GET /api/jobs/{job_id}` in `src/api/routes.py`.
- **Tests:** `tests/test_job_manager.py` (5 unit/API tests passing).
