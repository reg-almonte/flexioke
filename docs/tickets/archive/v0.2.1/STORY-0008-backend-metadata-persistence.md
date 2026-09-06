---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: in-review
---

# STORY-0008: Backend Song Metadata Model, Persistence & Patch API

## Parent Epic
- `docs/tickets/EPIC-0003-karaoke-metadata-and-stage-enhancements.md`

## What it delivers
Extends the backend data layer and REST API to support structured song metadata (`title` and `artist`). Enables updating song details via a `PATCH` endpoint, while ensuring 100% backward compatibility for existing `job.json` records without data loss.

## Acceptance Criteria
- [x] Backend data models accept and return `artist` alongside `title`.
- [x] Existing jobs without an `artist` field load without validation errors, defaulting `artist` to `null`/empty string.
- [x] `PATCH /api/jobs/{job_id}` allows updating `title` and `artist`, persisting changes to `job.json`.
- [x] Comprehensive unit tests verify serialization, deserialization, backward compatibility, and endpoint behavior.

## Tasks
- [x] TASK-0019: Model & JobStore Artist Field Extension with Legacy Deserialization
- [x] TASK-0020: Song Metadata Update REST Endpoint (PATCH /api/jobs/{job_id})

## Blocked by
- None (can start immediately)

