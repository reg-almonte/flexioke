---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0040: Direct Audio URL Downloader Endpoint & Ingestion Worker

## Parent Story
- `docs/tickets/STORY-0017-direct-audio-url-and-smart-naming.md`

## What to build
Build backend endpoint `POST /api/jobs/download-url` that accepts `{ "url": "https://..." }`, validates syntax, streams audio to `./data/jobs/{job_id}/input.mp3` with magic-byte/MIME validation (max 100MB), creates a `JobRecord` with `status: QUEUED`, and updates Stem Studio UI to replace YouTube card with Audio URL Ingestion.

## Acceptance Criteria
- [ ] `POST /api/jobs/download-url` accepts valid audio URLs and returns HTTP 202.
- [ ] Download progress is streamed and non-audio files or oversized payloads trigger HTTP 400.
- [ ] Stem Studio UI provides URL input field with download progress feedback.

## Blocked by
- None (can start immediately)
