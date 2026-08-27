---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: pending
---

# TASK-0013: Lyrics File Store & Pydantic Models

## Parent Story
- `STORY-0005-lyrics-storage-api.md`

## What to build
Define Pydantic models for lyrics requests/responses (`LyricsResponse`, `LyricsUpdateRequest`) and implement file-based helper functions in `JobManager` to read and atomically write `.lrc` files in the job's directory.

## Acceptance Criteria
- [ ] Pydantic models validate lyrics request payloads.
- [ ] File store helper functions read and write `.lrc` files with atomic write semantics.
- [ ] Unit tests verify file reading, writing, and missing lyrics handling.

## Blocked by
- None
