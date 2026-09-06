---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: completed
---

# STORY-0033: Immersive YouTube-Style Fullscreen Karaoke Stage

## Parent Epic
- `docs/tickets/EPIC-0010-ui-and-stage-experience-enhancements.md`

## What it delivers
Transforms the Karaoke Stage into an edge-to-edge cinema display (`100vw × 100vh`) with floating translucent glassmorphism top header and bottom transport overlays that automatically fade out along with the mouse cursor after 3 seconds of inactivity during playback, while providing double-click and hotkey fullscreen toggles.

## Acceptance Criteria
- [x] Fullscreen mode expands the lyric stage across the full viewport with cinema backdrop.
- [x] Top info pill (*Now Singing* / *Up Next*) and bottom transport bar float seamlessly over the stage.
- [x] During active playback in fullscreen, floating chrome and mouse cursor automatically fade out after 3 seconds of inactivity.
- [x] Moving the mouse, touching the screen, or pressing keys immediately restores visibility and resets the timer.
- [x] Double-clicking the stage canvas or pressing `F` toggles fullscreen mode.
- [x] 100% automated test coverage with zero regressions.

## Tasks
- [x] TASK-0069: In-Place Cinema Fullscreen & Floating Glassmorphism Chrome
- [x] TASK-0070: Inactivity Auto-Hide Engine, Cursor Hiding & Stage Shortcuts

## Blocked by
- `docs/tickets/STORY-0032-modular-svg-icon-dictionary.md`
