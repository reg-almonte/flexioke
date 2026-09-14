---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: in-review
---

# TASK-0074: Side A/B Ingestion Endpoints & Job Model Extension

## Parent Story
- `docs/tickets/STORY-0036-side-ab-dual-track-ingestion-and-playback.md`

## What to build
Build the backend Side A/B dual-track upload endpoints and data model extensions:
- Extend `SourceType` enum with `SIDE_AB = "side_ab"`.
- Implement `POST /api/jobs/upload-side-ab` accepting `file_side_b` (required), optional `file_side_a`, `title`, and `artist`.
- Save audio files directly into `/data/jobs/{id}/`, map `stems["instrumental"]` (Side B) and `stems["lead_vocals"]` (Side A if present), and set `status: JobStatus.COMPLETED` with `progress: 100` immediately without queuing separation tasks.
- Implement `POST /api/jobs/{id}/attach-side-a` to attach a vocal track to an existing Side B track.
- Add UI upload option in Stem Studio to switch between "Standard AI Separation" and "Direct Side A/B (Instrumental & Vocal)".

## Acceptance Criteria
- [x] `POST /api/jobs/upload-side-ab` creates instant completed tracks with proper stems.
- [x] `POST /api/jobs/{id}/attach-side-a` attaches Side A and updates stem mapping.
- [x] Stem Studio provides an intuitive dual-file upload interface.
- [x] Automated API and model integration tests pass 100%.

## Blocked by
- None (can start immediately in parallel).
