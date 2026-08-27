---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0008: Song Library Indexing & Search API

## Parent Story
- `STORY-0003-song-library-playback-queue.md`

## What to build
Implement the Song Library indexing service and `GET /api/jobs` endpoint to list all completed jobs with metadata (title, duration, source, stems, timestamp), supporting query parameter filtering (`?q=...` and `?status=...`).

## Acceptance Criteria
- [ ] `GET /api/jobs` returns a JSON list of all completed songs with stem URLs and metadata.
- [ ] Query parameter `?q=<term>` filters songs case-insensitively by title or source name.
- [ ] Cached index in memory updates automatically when new jobs complete.
- [ ] Unit/API tests verify library listing, filtering, and indexing accuracy.

## Blocked by
- TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager
