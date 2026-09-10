---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: pending
---

# STORY-0036: Direct Side A / Side B Dual-Track Ingestion & Vocal Hot-Swapping

## Parent Epic
- `docs/tickets/EPIC-0011-video-backgrounds-stage-geometry-and-side-ab.md`

## What it delivers
Provides a direct dual-track upload flow for pre-separated studio audio files: Side B (Instrumental only) and optional Side A (Vocal / Original version). Tracks bypass AI stem separation and are ready immediately. During playback, the Lead Vocal button cleanly hot-swaps between Side A and Side B audio streams in perfect sync, and button states adapt for single-sided tracks.

## Acceptance Criteria
- [ ] Users can upload Side B (Instrumental) + optional Side A (Vocal) directly via Stem Studio.
- [ ] Side A/B tracks are created immediately with `status: completed` and `progress: 100%` (bypassing AI separation tasks).
- [ ] Users can attach Side A to an existing Side B song via Song Details modal.
- [ ] Lead Vocal button hot-swaps between Side A and Side B in lockstep with zero latency or desync.
- [ ] Single-sided tracks gracefully lock the Lead Vocal toggle (`Lead: OFF (Side B Only)` or `Lead: ON (Side A Only)`).
- [ ] Backing vocal toggle is locked to `Backing: N/A` for Side A/B songs.
- [ ] **Mandatory Story Milestone Gate:** Requires explicit human manual verification in the browser before completing the epic.

## Tasks
- [ ] TASK-0074: Side A/B Ingestion Endpoints & Job Model Extension
- [ ] TASK-0075: Dual-Stream WebAudio Hot-Swapping & Dynamic Vocal Toggles

## Blocked by
- None (can start immediately in parallel).
