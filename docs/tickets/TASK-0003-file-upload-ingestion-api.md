---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0003: File Upload Ingestion API & Audio Validation

## Parent Story
- `STORY-0001-backend-foundation-ingestion.md`

## What to build
Implement the `POST /api/jobs/upload` endpoint to receive audio file uploads, validate file extension and size constraints (max 100MB), extract display title from filename, save the input file into the job folder, and register the job in the queue.

## Acceptance Criteria
- [x] `POST /api/jobs/upload` accepts `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` files up to 100MB.
- [x] Returns HTTP 202 with `job_id` and initial `queued` state upon successful upload.
- [x] Rejects files over 100MB or invalid non-audio formats with HTTP 400 and clear error message.
- [x] Unit/API tests verify valid uploads and error edge cases.

## Blocked by
- TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager

## Implementation
- **Branch:** `story/STORY-0001-backend-foundation-ingestion`
- **Validator:** `src/services/audio_validator.py` with extension whitelist, 100MB size limit, and title sanitization.
- **Endpoint:** `POST /api/jobs/upload` in `src/api/routes.py`.
- **Tests:** `tests/test_upload_api.py` (4 tests passing).
