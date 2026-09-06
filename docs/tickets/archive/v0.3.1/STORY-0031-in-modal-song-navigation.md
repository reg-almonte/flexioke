---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: completed
---

# STORY-0031: In-Modal Song Navigation & Dirty Changes Guard

## Parent Epic
- `docs/tickets/EPIC-0010-ui-and-stage-experience-enhancements.md`

## What it delivers
Allows users to seamlessly navigate between consecutive songs inside the Song Details & Lyrics editor modal using Previous (`◀`) and Next (`▶`) controls and hotkeys (`Alt + Left/Right`), while protecting unsaved metadata and lyric modifications with a confirmation guard.

## Acceptance Criteria
- [x] Users can click Previous and Next buttons in the modal header to navigate between songs in the current view's list.
- [x] Active track position badge (e.g., `Track 4 of 18`) accurately reflects current index in the active list context.
- [x] Previous button is disabled on the first song; Next button is disabled on the last song.
- [x] If user makes unsaved edits to Title, Artist, or Lyrics and attempts to navigate or close the modal, a confirmation prompt prevents accidental loss.
- [x] 100% automated test coverage with zero regressions.

## Tasks
- [x] TASK-0065: Modal Navigation Context & Track Position Counter
- [x] TASK-0066: Unsaved Edits Interceptor & Keyboard Shortcuts

## Blocked by
- None (can start immediately)
