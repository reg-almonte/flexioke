---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: pending
---

# TASK-0027: Lyrics Stage Background Click-to-Play/Pause with Bounded Lyric Pills

## Parent Story
- `docs/tickets/STORY-0011-simultaneous-stage-header-and-stage-click.md`

## What to build
Implement event delegation on the `#karaoke-lyrics-stage` background so clicking anywhere on the stage toggles playback Play/Pause. Style lyric line elements as bounded inline-block pills with `stopPropagation()` on direct line clicks to ensure clicking text seeks timestamp while clicking around text triggers Play/Pause.

## Acceptance Criteria
- [ ] Clicking the lyrics stage background toggles playback between Play and Pause.
- [ ] Lyric line pills have bounded click boundaries.
- [ ] Clicking a lyric line seeks directly to that line time without triggering the stage background toggle.

## Blocked by
- None (can start immediately in parallel)
