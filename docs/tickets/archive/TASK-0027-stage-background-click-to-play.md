---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# TASK-0027: Lyrics Stage Background Click-to-Play/Pause with Bounded Lyric Pills

## Parent Story
- `docs/tickets/STORY-0011-simultaneous-stage-header-and-stage-click.md`

## What to build
Implement event delegation on the `#karaoke-lyrics-stage` background so clicking anywhere on the stage toggles playback Play/Pause. Style lyric line elements as bounded inline-block pills with `stopPropagation()` on direct line clicks to ensure clicking text seeks timestamp while clicking around text triggers Play/Pause.

## Acceptance Criteria
- [x] Clicking the lyrics stage background toggles playback between Play and Pause.
- [x] Lyric line pills have bounded click boundaries.
- [x] Clicking a lyric line seeks directly to that line time without triggering the stage background toggle.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0011-simultaneous-stage-header-and-stage-click`
- Changes: Added `.karaoke-line-row` container and `.karaoke-line` bounded inline-block pill styles in `styles.css`, hooked up `togglePlayPause()` on `#karaoke-lyrics-stage` background clicks with `e.stopPropagation()` on line clicks in `karaoke.js`, and added integration test in `tests/test_karaoke_stage.py`.

