---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0004: YouTube URL Ingestion Engine via yt-dlp

## Parent Story
- `STORY-0001-backend-foundation-ingestion.md`

## What to build
Implement the `POST /api/jobs/youtube` endpoint and audio downloader service using `yt-dlp` to validate YouTube URLs, enforce 15-minute duration limits, extract video title/metadata, download the best audio stream, and save it as the job input file.

## Acceptance Criteria
- [x] `POST /api/jobs/youtube` accepts valid YouTube URLs and returns HTTP 202 with `job_id`.
- [x] Background worker executes `yt-dlp` to extract title, duration, and download audio into `./data/jobs/{job_id}/input.mp3`.
- [x] Rejects invalid URLs, restricted/private videos, or audio exceeding 15 minutes with helpful error messaging.
- [x] Unit/integration tests cover valid URL processing and failure handling.

## Blocked by
- TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager

## Implementation
- **Branch:** `story/STORY-0001-backend-foundation-ingestion`
- **Service:** `src/services/youtube_downloader.py` wrapping `yt-dlp` with regex URL checking, 15-min audio duration validation, and metadata extraction.
- **Endpoint:** `POST /api/jobs/youtube` in `src/api/routes.py`.
- **Tests:** `tests/test_youtube_api.py` (3 tests passing, 14 suite-wide).
