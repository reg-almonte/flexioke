---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0007: End-to-End Separation Worker Orchestration & Stem Streaming Endpoints

## Parent Story
- `STORY-0002-two-stage-stem-separation.md`

## What to build
Integrate Stage 1 and Stage 2 into the asynchronous job runner, update progress stages (`separating_stage_1` $\rightarrow$ `separating_stage_2` $\rightarrow$ `completed`), populate stem URLs in metadata, and expose stem streaming endpoints `GET /api/jobs/{job_id}/stems/{stem_type}`.

## Acceptance Criteria
- [ ] Background pipeline orchestrates full 2-stage workflow from ingestion to final MP3 stems.
- [ ] `GET /api/jobs/{job_id}/stems/{stem_type}` streams `instrumental`, `lead_vocals`, and `backing_vocals` with appropriate audio headers.
- [ ] Catches pipeline errors, cleans temporary intermediate files, and updates job status to `failed` with error reason.
- [ ] End-to-end integration tests verify full pipeline execution and stem streaming.

## Blocked by
- TASK-0006: Stage 2 Karaoke Separation Engine (UVR MDX-Net Kara 2) & MP3 Encoding
