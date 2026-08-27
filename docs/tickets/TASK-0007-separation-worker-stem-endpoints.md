---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0007: End-to-End Separation Worker Orchestration & Stem Streaming Endpoints

## Parent Story
- `STORY-0002-two-stage-stem-separation.md`

## What to build
Integrate Stage 1 and Stage 2 into the asynchronous job runner, update progress stages (`separating_stage_1` $\rightarrow$ `separating_stage_2` $\rightarrow$ `completed`), populate stem URLs in metadata, and expose stem streaming endpoints `GET /api/jobs/{job_id}/stems/{stem_type}`.

## Acceptance Criteria
- [x] Background pipeline orchestrates full 2-stage workflow from ingestion to final MP3 stems.
- [x] `GET /api/jobs/{job_id}/stems/{stem_type}` streams `instrumental`, `lead_vocals`, and `backing_vocals` with appropriate audio headers.
- [x] Catches pipeline errors, cleans temporary intermediate files, and updates job status to `failed` with error reason.
- [x] End-to-end integration tests verify full pipeline execution and stem streaming.

## Blocked by
- TASK-0006: Stage 2 Karaoke Separation Engine (UVR MDX-Net Kara 2) & MP3 Encoding

## Implementation
- **Branch:** `story/STORY-0002-two-stage-stem-separation`
- **Orchestration:** `src/services/pipeline.py` managing sequential Stage 1 $\rightarrow$ Stage 2 $\rightarrow$ MP3 encoding, status progression, temporary file cleanup, and error recovery.
- **Endpoints:** `GET /api/jobs/{job_id}/stems/{stem_type}` for streaming audio stems.
- **Tests:** `tests/test_pipeline_and_stems.py` (2 integration tests passing, 20 suite-wide).
