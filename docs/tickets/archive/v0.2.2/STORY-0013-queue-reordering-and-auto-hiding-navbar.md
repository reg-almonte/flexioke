---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# STORY-0013: Queue Reordering API, Sidebar Reorganization & Auto-Hiding Navbar

## Parent Epic
- `docs/tickets/EPIC-0004-karaoke-stage-transport-and-queue-refinements.md`

## What it delivers
Provides seamless queue management by positioning the Playback Queue above the Song Library in Karaoke Mode, adding directional `▲` and `▼` queue reordering buttons backed by an atomic backend endpoint with live stage header updates, and implementing an auto-hiding application navbar that reveals on top hover.

## Acceptance Criteria
- [x] Backend `POST /api/queue/reorder` endpoint atomically swaps queued tracks up or down under thread lock.
- [x] Karaoke sidebar positions Playback Queue at the top and Song Library below.
- [x] Queued song cards include `▲` and `▼` buttons that dynamically update order in real time.
- [x] Moving a song to the top of the queue immediately updates the "Up Next" stage header.
- [x] Top application header smoothly hides off-screen and reveals when the cursor hovers near the top viewport edge.

## Tasks
- [x] TASK-0030: Backend Queue Reordering Endpoint (POST /api/queue/reorder)
- [x] TASK-0031: Karaoke Sidebar Reorganization (Queue on Top) with Reordering Controls
- [x] TASK-0032: Top Application Header Auto-Hide & Reveal with Top Hover Sensor

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0013-queue-reordering-and-auto-hiding-navbar`
- Completed TASK-0030, TASK-0031, and TASK-0032 with all 70 integration tests passing.

