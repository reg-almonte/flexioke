---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: completed
---

# TASK-0069: In-Place Cinema Fullscreen & Floating Glassmorphism Chrome

## Parent Story
- `docs/tickets/STORY-0033-youtube-style-fullscreen-karaoke-stage.md`

## What to build
Implement the full-screen cinema layout and floating glassmorphism overlays:
- Update `#karaoke-stage-card` to support `.karaoke-cinema-fullscreen` styling expanding to `fixed inset-0 z-[9999] w-screen h-screen bg-[#030712]`.
- Position the top header as a floating glassmorphism pill (`top-4 left-1/2 -translate-x-1/2 backdrop-blur-md bg-surface-950/80 border border-slate-800/80 rounded-2xl p-3 shadow-2xl`).
- Position the bottom transport bar as a floating glassmorphism bar (`bottom-4 left-1/2 -translate-x-1/2 backdrop-blur-md bg-surface-950/85 border border-slate-800/80 rounded-2xl p-3.5 shadow-2xl`).
- Add an explicit Exit Fullscreen button (`#karaoke-exit-fullscreen-btn`) in the floating header.

## Acceptance Criteria
- [x] Entering fullscreen positions top and bottom chrome as floating overlays over the lyrics stage.
- [x] Lyrics container expands to full viewport height behind the floating bars.
- [x] Exiting fullscreen cleanly restores original sidebar-adjacent layout.

## Blocked by
- `docs/tickets/TASK-0068-ui-iconography-overhaul-and-tooltips.md`
