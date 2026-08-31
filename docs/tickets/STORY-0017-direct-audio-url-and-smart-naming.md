---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# STORY-0017: Direct Audio URL Ingestion & Smart Title/Artist Parsing

## Parent Epic
- `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

## What it delivers
Allows users to enter direct HTTP/HTTPS audio file URLs for background downloading and automatic stem separation, replacing unreliable YouTube scraping, and automatically extracts Title and Artist from `<Song Title> - <Artist>.<ext>` filenames.

## Acceptance Criteria
- [x] Direct audio URLs are downloaded asynchronously with MIME/magic byte validation and 100MB max limit.
- [x] Filenames containing `" - "` automatically split into `title` and `artist`, normalizing underscores and leading track numbers.

## Tasks
- [x] TASK-0040: Direct Audio URL Downloader Endpoint & Ingestion Worker
- [x] TASK-0041: Smart Filename Delimiter (Title - Artist) Parser

## Implementation
- Branch: `story/STORY-0017-direct-audio-url-and-smart-naming`
- Both TASK-0040 and TASK-0041 complete and covered by 93 automated tests.

## Blocked by
- None (can start immediately)
