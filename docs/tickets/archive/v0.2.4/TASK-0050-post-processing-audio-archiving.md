---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0050: Post-Separation Raw Input Audio Archiving to ./data/archive/

## Parent Story
- `docs/tickets/STORY-0021-stem-zip-export-and-cleanup.md`

## What to build
Update the stem separation pipeline coordinator so that upon successful completion of Stage 2 separation, the raw input audio file `./data/jobs/{job_id}/input.mp3` is moved to `./data/archive/{job_id}_{sanitized_source_name}.mp3`, creating `./data/archive/` if it does not exist.

## Acceptance Criteria
- [x] Input audio is moved to `./data/archive/` upon successful separation.
- [x] Job folder retains only stem MP3s and metadata/lyrics.

## Implementation
- Added post-separation move of raw input audio to `./data/archive/{job_id}_{clean_source}` in `src/services/pipeline.py`.
- Verified in `tests/test_pipeline_and_stems.py`.

## Blocked by
- None (can start immediately)
