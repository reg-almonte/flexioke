---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# STORY-0017: Direct Audio URL Ingestion & Smart Title/Artist Parsing

## Parent Epic
- `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

## What it delivers
Allows users to enter direct HTTP/HTTPS audio file URLs for background downloading and automatic stem separation, replacing unreliable YouTube scraping, and automatically extracts Title and Artist from `<Song Title> - <Artist>.<ext>` filenames.

## Acceptance Criteria
- [ ] Direct audio URLs are downloaded asynchronously with MIME/magic byte validation and 100MB max limit.
- [ ] Filenames containing `" - "` automatically split into `title` and `artist`, normalizing underscores and leading track numbers.

## Tasks
- [ ] TASK-0040: Direct Audio URL Downloader Endpoint & Ingestion Worker
- [ ] TASK-0041: Smart Filename Delimiter (Title - Artist) Parser

## Blocked by
- None (can start immediately)
