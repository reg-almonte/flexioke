---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: in-review
---

# TASK-0052: Background Separation Pipeline Lyrics Auto-Sync

## Parent Story
- `docs/tickets/STORY-0022-lrclib-client-and-pipeline-auto-sync.md`

## What to build
Integrate the LRCLIB client into `run_separation_pipeline` in `src/services/pipeline.py`. If `lyrics.lrc` does not exist for the job, automatically query LRCLIB using the parsed Title and Artist metadata and persist the synchronized `.lrc` text to `./data/jobs/{job_id}/lyrics.lrc`.

## Acceptance Criteria
- [x] During pipeline separation, if `lyrics.lrc` is missing, auto-fetches from LRCLIB and writes file.
- [x] Does not overwrite existing non-empty `lyrics.lrc` files.
- [x] Network failures or missing lyrics are non-fatal and log warnings without stopping separation.

## Implementation
- Integrated `lrclib_client.get_lyrics()` inside `run_separation_pipeline` in `src/services/pipeline.py`.
- Preserves existing lyrics files and safely writes retrieved `.lrc` content.
- Verified in `tests/test_pipeline_and_stems.py`.

## Blocked by
- `docs/tickets/TASK-0051-lrclib-client-module-and-proxy-endpoints.md`
