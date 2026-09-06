---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# TASK-0066: Unsaved Edits Interceptor & Keyboard Shortcuts

## Parent Story
- `docs/tickets/STORY-0031-in-modal-song-navigation.md`

## What to build
Implement dirty state tracking and keyboard navigation:
- Track baseline values of Title, Artist, and Lyrics on load; update dirty flag on input events.
- Intercept Previous/Next button clicks, Close button, and `Esc` key when dirty, displaying a confirmation prompt to prevent unintended data loss.
- Bind `Alt + Left Arrow` and `Alt + Right Arrow` (as well as Left/Right arrow keys when inputs are not focused) to navigate songs.
- Clear dirty flag upon successful save.

## Acceptance Criteria
- [ ] Confirmation prompt appears when attempting to navigate or close with unsaved edits.
- [ ] Discarding proceeds with navigation/closure; cancelling remains on the active song.
- [ ] Keyboard shortcuts trigger song navigation cleanly.

## Blocked by
- `docs/tickets/TASK-0065-modal-navigation-context-and-counter.md`
