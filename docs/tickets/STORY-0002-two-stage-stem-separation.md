---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# STORY-0002: 2-Stage Audio Stem Separation Pipeline

## Parent Epic
- `EPIC-0001-stem-separation-player.md`

## What it delivers
An asynchronous deep learning audio separation pipeline that transforms uploaded or downloaded audio into 3 distinct MP3 stems: `Instrumental`, `Lead Vocals`, and `Backing Vocals` using Mel-Band RoFormer and UVR MDX-Net Karaoke models, exposing streaming endpoints for the resulting tracks.

## Acceptance Criteria
- [ ] Stage 1 executes Mel-Band RoFormer to produce `instrumental` and `vocals` stems.
- [ ] Stage 2 executes UVR MDX-Net Karaoke on `vocals` to produce `lead_vocals` and `backing_vocals` stems.
- [ ] All 3 stems are properly formatted and encoded as MP3 files.
- [ ] Job status updates dynamically across stages (`separating_stage_1`, `separating_stage_2`, `completed`).
- [ ] Stems are streamable via `GET /api/jobs/{job_id}/stems/{stem_type}`.

## Tasks
- [ ] TASK-0005: Stage 1 Separation Engine (Mel-Band RoFormer Integration)
- [ ] TASK-0006: Stage 2 Karaoke Separation Engine (UVR MDX-Net Kara 2) & MP3 Encoding
- [ ] TASK-0007: End-to-End Separation Worker Orchestration & Stem Streaming Endpoints

## Blocked by
- STORY-0001: Backend Foundation, Job Manager & Ingestion APIs
