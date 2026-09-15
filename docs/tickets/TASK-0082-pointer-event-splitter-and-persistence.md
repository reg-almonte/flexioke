---
status: approved
approved_by: user
approved_at: 2026-09-16
implementation: pending
---

# TASK-0082: PointerEvent Splitter Controller & Persistence

## Parent Story
- `docs/tickets/STORY-0040-vscode-style-activity-bar-and-resizable-panel.md`

## What to build
Build the interactive splitter controller and `localStorage` persistence layer:
- Add `#karaoke-splitter-handle` between sidebar content and main stage with `col-resize` hover cursor and visual divider line.
- Implement pointer event handling (`pointerdown`, `setPointerCapture`, `pointermove`, `pointerup`) with width clamping between 48px and 50vw.
- Add double-click handler on splitter handle to reset width to default 320px.
- Implement global keyboard shortcuts (`Ctrl+B` / `Cmd+B` / `Alt+S`) to toggle sidebar collapse/expand.
- Persist and synchronously hydrate `{ width, activeTab, collapsed }` from `localStorage` (`flexioke_karaoke_sidebar_state`).

## Acceptance Criteria
- [ ] Dragging splitter handle smoothly resizes the sidebar with pointer capture.
- [ ] Double-click resets sidebar width to 320px.
- [ ] Keyboard shortcuts (`Ctrl+B`, `Cmd+B`) toggle collapse.
- [ ] Panel state is restored on page load from `localStorage` with zero FOUC.

## Blocked by
- `TASK-0081`
