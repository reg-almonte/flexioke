---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: pending
---

# TASK-0018: Karaoke Quick Vocal Toggles & Smart Play Interruption Prompt

## Parent Story
- `STORY-0007-karaoke-page-synchronized-stage.md`

## What to build
Add quick Lead Vocals and Backing Vocals mute/unmute toggle pill buttons to the Karaoke transport, and implement the smart play interruption modal that prompts the user when clicking "Play" while another song is currently playing.

## Acceptance Criteria
- [ ] Quick Lead Vocals toggle instantly mutes/unmutes the lead vocal stem for solo singing.
- [ ] Quick Backing Vocals toggle instantly mutes/unmutes backing harmonies.
- [ ] Clicking "Play" during active playback shows confirmation dialog; proceeding plays new song without modifying the queued songs.

## Blocked by
- TASK-0017: Real-Time LRC Parser & Synchronized Center-Stage Lyrics Display
