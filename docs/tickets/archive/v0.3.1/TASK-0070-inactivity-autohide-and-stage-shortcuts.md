---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: completed
---

# TASK-0070: Inactivity Auto-Hide Engine, Cursor Hiding & Stage Shortcuts

## Parent Story
- `docs/tickets/STORY-0033-youtube-style-fullscreen-karaoke-stage.md`

## What to build
Implement the auto-hide inactivity controller and interaction shortcuts:
- In `KaraokeStageManager`, initialize a 3000ms inactivity timer during active playback in fullscreen mode.
- When idle for 3s during playback, apply `.karaoke-chrome-hidden` (`opacity: 0; pointer-events: none; transition: opacity 0.4s ease`) and `.karaoke-cursor-hidden` (`cursor: none`).
- Reset timer and restore visibility on `mousemove`, `touchstart`, or `keydown`.
- Keep controls continuously visible when paused or stopped.
- Attach double-click listener to `#karaoke-lyrics-stage` and bind `F` key to toggle fullscreen mode.

## Acceptance Criteria
- [x] Controls and mouse cursor auto-hide after 3 seconds of inactivity during fullscreen playback.
- [x] User movement or keypress immediately wakes floating controls and resets the timer.
- [x] Double-clicking the lyrics stage or pressing `F` toggles fullscreen mode.

## Blocked by
- `docs/tickets/TASK-0069-cinema-fullscreen-floating-chrome.md`
