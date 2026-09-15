---
status: approved
approved_by: user
approved_at: 2026-09-16
implementation: pending
---

# TASK-0086: Universal Focus-Guarded Spacebar Play/Pause Shortcut

## Parent Story
- `docs/tickets/STORY-0042-fullscreen-cinema-scaling-and-spacebar-control.md`

## What to build
Implement universal focus-guarded Spacebar play/pause handler:
- Register global `keydown` listener on `window`.
- Check if `event.code === 'Space'`.
- Inspect `document.activeElement` for `INPUT`, `TEXTAREA`, `SELECT`, and `isContentEditable` attributes; if found, pass event through untouched.
- If outside form inputs, invoke `event.preventDefault()` to stop browser page scroll jumps and execute active player Play/Pause toggle in Karaoke Mode or Stem Studio.

## Acceptance Criteria
- [ ] Spacebar toggles Play/Pause across Karaoke Mode and Stem Studio.
- [ ] Spacebar allows typing spaces in search bars, lyrics editor, notes modal, and rename inputs without toggling playback.
- [ ] Page scrolling on Spacebar press is eliminated.

## Blocked by
- None (can start immediately).
