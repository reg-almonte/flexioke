---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# STORY-0007: Dedicated Karaoke Player Page & Synchronized Stage

## Parent Epic
- `EPIC-0002-karaoke-lyrics-mode.md`

## What it delivers
A dedicated full-screen Karaoke Mode tab featuring synchronized center-stage lyrics with active line magnification, smooth vertical auto-scroll, quick Lead/Backing vocal toggles, shared library/queue, and smart play interruption alerts.

## Acceptance Criteria
- [x] Top navigation bar enables instant switching between "Stem Studio" and "Karaoke Mode" without pausing audio.
- [x] Active lyric line is highlighted and smoothly centered in real time according to playback timecode.
- [x] Fallbacks gracefully handle missing lyrics and plain text transcripts.
- [x] Quick Lead and Backing vocal buttons toggle vocal stems instantly.
- [x] Attempting to play a song during active playback pauses and prompts for user confirmation while preserving the queue.

## Tasks
- [x] TASK-0016: Top Navigation Bar Tabs (Stem Studio vs Karaoke Mode)
- [x] TASK-0017: Real-Time LRC Parser & Synchronized Center-Stage Lyrics Display
- [x] TASK-0018: Karaoke Quick Vocal Toggles & Smart Play Interruption Prompt

## Blocked by
- STORY-0005: Lyrics Storage Service & API Endpoints
- STORY-0006: Frontend Lyrics Management & Editor UI

## Implementation Summary
- **Branch:** `story/STORY-0007-karaoke-page-synchronized-stage`
- **UI:** `src/static/index.html`, `src/static/app.js`, `src/static/karaoke.js`, `src/static/library_queue.js`.
- **Tests:** 47 unit & integration tests passing across all test suites.
