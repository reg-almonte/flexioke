---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: pending
---

# TASK-0017: Real-Time LRC Parser & Synchronized Center-Stage Lyrics Display

## Parent Story
- `STORY-0007-karaoke-page-synchronized-stage.md`

## What to build
Build `src/static/karaoke.js` implementing the `LrcParser` and `KaraokeLyricsRenderer` to parse timestamped lyrics, listen to player timeupdates, illuminate the active singing line, and auto-scroll the center stage smoothly.

## Acceptance Criteria
- [ ] Accurately parses standard `[mm:ss.xx]` timestamped LRC format.
- [ ] Highlights active lyric line and applies smooth auto-scroll to keep line centered.
- [ ] Displays appropriate fallback messages for missing lyrics or plain-text lyrics.

## Blocked by
- TASK-0015: Song Library Lyrics Editor Modal & Paste UI
- TASK-0016: Top Navigation Bar Tabs (Stem Studio vs Karaoke Mode)
