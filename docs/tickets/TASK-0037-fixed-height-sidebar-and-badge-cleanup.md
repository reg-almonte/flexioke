---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0037: Fixed 3-Card Height Playback Queue & Compact Library with "Stems Ready" Removal

## Parent Story
- `docs/tickets/STORY-0016-fixed-sidebar-and-song-catalog-modal.md`

## What to build
Set the Playback Queue container to a fixed height (`h-[196px]`) accommodating 3 visible songs with a centered empty state when empty and custom scrollbar for overflow. Adjust the Song Library container height to `h-[210px]` (3 cards tall). Remove the `"Stems ready"` badge from library song cards.

## Acceptance Criteria
- [ ] Playback Queue container maintains a fixed height of 3 songs regardless of item count.
- [ ] Song Library container displays 3 visible cards tall.
- [ ] Song cards display Title and Artist without the `"Stems ready"` text.

## Blocked by
- None (can start immediately in parallel)
