---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: pending
---

# STORY-0007: Dedicated Karaoke Player Page & Synchronized Stage

## Parent Epic
- `EPIC-0002-karaoke-lyrics-mode.md`

## What it delivers
A dedicated full-screen Karaoke Mode tab featuring synchronized center-stage lyrics with active line magnification, smooth vertical auto-scroll, quick Lead/Backing vocal toggles, shared library/queue, and smart play interruption alerts.

## Acceptance Criteria
- [ ] Top navigation bar enables instant switching between "Stem Studio" and "Karaoke Mode" without pausing audio.
- [ ] Active lyric line is highlighted and smoothly centered in real time according to playback timecode.
- [ ] Fallbacks gracefully handle missing lyrics and plain text transcripts.
- [ ] Quick Lead and Backing vocal buttons toggle vocal stems instantly.
- [ ] Attempting to play a song during active playback pauses and prompts for user confirmation while preserving the queue.

## Tasks
- [ ] TASK-0016: Top Navigation Bar Tabs (Stem Studio vs Karaoke Mode)
- [ ] TASK-0017: Real-Time LRC Parser & Synchronized Center-Stage Lyrics Display
- [ ] TASK-0018: Karaoke Quick Vocal Toggles & Smart Play Interruption Prompt

## Blocked by
- STORY-0005: Lyrics Storage Service & API Endpoints
- STORY-0006: Frontend Lyrics Management & Editor UI
