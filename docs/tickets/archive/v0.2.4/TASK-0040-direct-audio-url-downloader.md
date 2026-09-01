---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0040: Direct Audio URL Downloader Endpoint & Ingestion Worker

## Parent Story
- `docs/tickets/STORY-0017-direct-audio-url-and-smart-naming.md`

## What to build
Build backend endpoint `POST /api/jobs/download-url` that accepts `{ "url": "https://..." }`, validates syntax, streams audio to `./data/jobs/{job_id}/input.mp3` with magic-byte/MIME validation (max 100MB), creates a `JobRecord` with `status: QUEUED`, and updates Stem Studio UI to replace YouTube card with Audio URL Ingestion.

## Acceptance Criteria
- [x] `POST /api/jobs/download-url` accepts valid audio URLs and returns HTTP 202.
- [x] Download progress is streamed and non-audio files or oversized payloads trigger HTTP 400.
- [x] Stem Studio UI provides URL input field with download progress feedback.

## Implementation
- Implemented `src/services/audio_downloader.py` with `validate_audio_url()` and streaming `download_audio_url()`.
- Implemented `POST /api/jobs/download-url` in `src/api/routes.py`.
- Updated Stem Studio Ingestion Card in `src/static/index.html` and `src/static/app.js` with `#tab-url-btn`, `#audio-url-input`, and `#submit-audio-url-btn`.
- Unit tests verified in `tests/test_audio_downloader.py` and `tests/test_audio_url_api.py`.

## Blocked by
- None (can start immediately)
