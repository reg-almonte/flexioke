---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# STORY-0011: Simultaneous Stage Header with CSS Marquee & Lyrics Stage Click-to-Play

## Parent Epic
- `docs/tickets/EPIC-0004-karaoke-stage-transport-and-queue-refinements.md`

## What it delivers
Presents both "Now Singing" and "Up Next" simultaneously across the stage header in a clean single-line `Title - Artist` layout that auto-scrolls marquee animations when overflowing, removes redundant toolbar font buttons, and enables intuitive click-to-play/pause on the stage background while preserving precise timestamp seeking on lyric lines.

## Acceptance Criteria
- [x] Top stage header displays both "Now Singing: [Title] - [Artist]" on the left and "Up Next: [Next Title] - [Next Artist]" on the right simultaneously.
- [x] When no songs are queued, the right header displays a clear placeholder ("Up Next: — (Queue Empty)").
- [x] Text overflowing header boundaries animates with a smooth CSS marquee effect.
- [x] `A-` / `A+` buttons removed from stage header (font scaling consolidated in Stage Settings).
- [x] Clicking the lyrics stage background toggles Play/Pause.
- [x] Clicking a lyric line seeks directly to that line timestamp without triggering the stage play/pause toggle.

## Tasks
- [x] TASK-0026: Dual Stage Header Layout with CSS Marquee on Overflow
- [x] TASK-0027: Lyrics Stage Background Click-to-Play/Pause with Bounded Lyric Pills

## Blocked by
- None (can start immediately)

## Implementation
- Branch: `story/STORY-0011-simultaneous-stage-header-and-stage-click`
- Complete implementation of TASK-0026 and TASK-0027.

