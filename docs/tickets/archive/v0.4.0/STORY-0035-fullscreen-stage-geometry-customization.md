---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: completed
---

# STORY-0035: Fullscreen Stage Geometry Customization

## Parent Epic
- `docs/tickets/EPIC-0011-video-backgrounds-stage-geometry-and-side-ab.md`

## What it delivers
Empowers users to customize the dimensions and vertical center position of the fullscreen lyrics stage (`#karaoke-lyrics-stage`) via intuitive sliders in Stage Settings, tailoring the layout to external screens, TVs, or projectors while leaving windowed mode unaffected.

## Acceptance Criteria
- [x] Sliders for Width (`60%–100%`), Height (`30vh–80vh`), and Vertical Offset (`-20%–+20%`) available in `#karaoke-settings-modal`.
- [x] Real-time DOM updates applied via CSS custom properties.
- [x] Scope isolation strictly enforces that windowed/default stage layout is unaffected.
- [x] Preferences persist across page reloads in `localStorage`.
- [x] **Mandatory Story Milestone Gate:** Requires explicit human manual verification in the browser before advancing to subsequent stories.

## Tasks
- [x] TASK-0073: Fullscreen Geometry CSS Variables & Stage Settings Sliders

## Blocked by
- None (can start immediately in parallel).
