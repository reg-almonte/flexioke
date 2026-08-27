---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# STORY-0001: Backend Foundation, Job Manager & Ingestion APIs

## Parent Epic
- `EPIC-0001-stem-separation-player.md`

## What it delivers
A reliable backend server foundation that accepts audio uploads and YouTube video URLs, verifies audio constraints, assigns unique job IDs, manages filesystem storage and metadata, and provides non-blocking job status polling endpoints.

## Acceptance Criteria
- [x] Backend server initializes cleanly with CORS and routing configuration.
- [x] Filesystem storage structure `./data/jobs/{job_id}/` is created and managed automatically.
- [x] Users can upload `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` files (up to 100MB) via `POST /api/jobs/upload`.
- [x] Users can submit valid YouTube links via `POST /api/jobs/youtube` and extract audio via `yt-dlp`.
- [x] Job status endpoint `GET /api/jobs/{job_id}` returns current processing stage, progress percentage, and error details if failed.

## Tasks
- [x] TASK-0001: Project Scaffolding, FastAPI Setup & Dependencies Configuration
- [x] TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager
- [x] TASK-0003: File Upload Ingestion API & Audio Validation
- [x] TASK-0004: YouTube URL Ingestion Engine via `yt-dlp`

## Blocked by
- None (can start immediately)

## Implementation Summary
- **Branch:** `story/STORY-0001-backend-foundation-ingestion`
- **Modules:** `src/main.py`, `src/models.py`, `src/api/routes.py`, `src/services/job_manager.py`, `src/services/audio_validator.py`, `src/services/youtube_downloader.py`.
- **Tests:** 14 unit and integration tests passing in `tests/`.
