---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# STORY-0016: Fixed-Height Sidebar Viewports, Scoped Permissions & Song Catalog Modal

## Parent Epic
- `docs/tickets/EPIC-0005-karaoke-stage-ux-and-song-catalog.md`

## What it delivers
Stabilizes the sidebar layout by fixing the Playback Queue to 3 cards tall with centered empty states, compacting the Song Library to 3 cards, removing the redundant "Stems ready" badge, restricting the "Edit Details / Lyrics" button strictly to Stem Studio, and introducing a full-screen Song Catalog Modal with instant client-side search, sorting, and 1-click Play Now / Add to Queue actions.

## Acceptance Criteria
- [x] Playback Queue container has a fixed 3-song height with no layout shift on queue addition/removal.
- [x] Song Library displays 3 cards tall and cards no longer show the "Stems ready" badge.
- [x] Edit Details / Lyrics button (`✏`) is rendered only in Stem Studio (Page 1) and completely removed from Karaoke Mode (Page 2 sidebar and Catalog Modal).
- [x] Expand button at the top right of the Karaoke Song Library opens the Song Catalog Modal.
- [x] Catalog Modal features instant search filter, clear button, sort dropdown (Title A-Z/Z-A, Artist A-Z, Recent), and direct Play Now and Add to Queue actions.
- [x] Modal can be closed via `Esc`, close button, or clicking the backdrop overlay.

## Tasks
- [x] TASK-0037: Fixed 3-Card Height Playback Queue & Compact Library with "Stems Ready" Removal
- [x] TASK-0038: Scoped Edit Button Visibility (Stem Studio Only)
- [x] TASK-0039: Expanded Song Catalog Modal with Instant Search, Sorting & 1-Click Actions

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0016-fixed-sidebar-and-song-catalog-modal`
- Delivered fixed 3-song height for Playback Queue (`h-[196px]`) and Song Library (`h-[210px]`).
- Stripped `"Stems ready"` text from library card rendering.
- Contextually restricted `.lyrics-btn` (`✏`) strictly to Stem Studio (`#view-studio`).
- Delivered `#song-catalog-modal` with search, sorting, and 1-click Play Now / Add to Queue actions.
- Full automated test suite passes (81/81 tests).

