---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager

## Parent Story
- `STORY-0001-backend-foundation-ingestion.md`

## What to build
Implement the core Job model, filesystem directory manager (`./data/jobs/{job_id}/`), JSON metadata serializer/deserializer (`job.json`), status polling handler, and bounded background worker executor for serializing resource-heavy separation jobs.

## Acceptance Criteria
- [ ] Unique UUID job directories are safely initialized.
- [ ] Job state transitions (`queued`, `downloading`, `separating_stage_1`, `separating_stage_2`, `completed`, `failed`) serialize to disk atomically.
- [ ] Status endpoint `GET /api/jobs/{job_id}` returns up-to-date status, progress percentage, stage description, and error details if applicable.
- [ ] Unit tests cover job creation, serialization, updates, and concurrency limits.

## Blocked by
- TASK-0001: Project Scaffolding, FastAPI Setup & Dependencies Configuration
