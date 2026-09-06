---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0018: Karaoke Quick Vocal Toggles & Smart Play Interruption Prompt

## Parent Story
- `STORY-0007-karaoke-page-synchronized-stage.md`

## What to build
Add quick Lead Vocals and Backing Vocals mute/unmute toggle pill buttons to the Karaoke transport, and implement the smart play interruption modal that prompts the user when clicking "Play" while another song is currently playing.

## Acceptance Criteria
- [x] Quick Lead Vocals toggle instantly mutes/unmutes the lead vocal stem for solo singing.
- [x] Quick Backing Vocals toggle instantly mutes/unmutes backing harmonies.
- [x] Clicking "Play" during active playback shows confirmation dialog; proceeding plays new song without modifying the queued songs.

## Blocked by
- TASK-0017: Real-Time LRC Parser & Synchronized Center-Stage Lyrics Display

## Implementation
- **Branch:** `story/STORY-0007-karaoke-page-synchronized-stage`
- **Karaoke Controls:** `src/static/karaoke.js` (`#karaoke-toggle-lead-btn`, `#karaoke-toggle-backing-btn`, `#karaoke-play-btn`, `#karaoke-skip-btn`, `#karaoke-volume-slider`).
- **Interruption Guard:** `src/static/library_queue.js` and `#play-confirm-modal` in `src/static/index.html` guarding active playback and preserving the existing playlist queue.
- **Tests:** `tests/test_karaoke_controls_and_interruption.py` (2 tests passing, 47 suite-wide).
