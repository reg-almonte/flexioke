---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0013: Lyrics File Store & Pydantic Models

## Parent Story
- `STORY-0005-lyrics-storage-api.md`

## What to build
Define Pydantic models for lyrics requests/responses (`LyricsResponse`, `LyricsUpdateRequest`) and implement file-based helper functions in `JobManager` to read and atomically write `.lrc` files in the job's directory.

## Acceptance Criteria
- [x] Pydantic models validate lyrics request payloads.
- [x] File store helper functions read and write `.lrc` files with atomic write semantics.
- [x] Unit tests verify file reading, writing, and missing lyrics handling.

## Blocked by
- None

## Implementation
- **Branch:** `story/STORY-0005-lyrics-storage-api`
- **Models:** `LyricsResponse`, `LyricsUpdateRequest` in `src/models.py`.
- **Service:** `JobManager.get_lyrics()` and `JobManager.save_lyrics()` in `src/services/job_manager.py` with regex timestamp detection and atomic temp-file replace.
- **Tests:** `tests/test_lyrics_store.py` (4 tests passing, 37 suite-wide).
