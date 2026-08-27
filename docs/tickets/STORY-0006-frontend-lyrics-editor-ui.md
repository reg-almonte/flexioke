---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# STORY-0006: Frontend Lyrics Management & Editor UI

## Parent Epic
- `EPIC-0002-karaoke-lyrics-mode.md`

## What it delivers
A clean modal editor in the web interface allowing users to view, paste, and save timestamped LRC or plain-text lyrics directly from the Song Library.

## Acceptance Criteria
- [x] Song library cards feature a lyrics action button.
- [x] Modal dialog allows pasting multi-line lyrics with formatting syntax hints.
- [x] Saving updates the server and refreshes the active lyrics view immediately.

## Tasks
- [x] TASK-0015: Song Library Lyrics Editor Modal & Paste UI

## Blocked by
- STORY-0005: Lyrics Storage Service & API Endpoints

## Implementation Summary
- **Branch:** `story/STORY-0006-frontend-lyrics-editor-ui`
- **UI:** `src/static/index.html`, `src/static/library_queue.js`.
- **Tests:** 42 unit & integration tests passing across all test suites.
