---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0003: File Upload Ingestion API & Audio Validation

## Parent Story
- `STORY-0001-backend-foundation-ingestion.md`

## What to build
Implement the `POST /api/jobs/upload` endpoint to receive audio file uploads, validate file extension and size constraints (max 100MB), extract display title from filename, save the input file into the job folder, and register the job in the queue.

## Acceptance Criteria
- [ ] `POST /api/jobs/upload` accepts `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` files up to 100MB.
- [ ] Returns HTTP 202 with `job_id` and initial `queued` state upon successful upload.
- [ ] Rejects files over 100MB or invalid non-audio formats with HTTP 400 and clear error message.
- [ ] Unit/API tests verify valid uploads and error edge cases.

## Blocked by
- TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager
