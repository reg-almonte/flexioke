---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: pending
---

# TASK-0023: Alternating "Now Singing" ⟷ "Up Next" Header & Remaining Time Badge

## Parent Story
- `docs/tickets/STORY-0010-stage-header-countdown-controls.md`

## What to build
Enhance the stage header in `src/static/karaoke_stage.js` and `src/templates/index.html`. Format the header to show `"Now Singing: [Title] • [Artist]"` and a time badge showing `MM:SS / MM:SS (-MM:SS remaining)`. If upcoming songs exist in the queue, run a timer that alternates between "Now Singing" and "Up Next: [Next Title] • [Next Artist]" using smooth CSS opacity cross-fades on a configurable interval.

## Acceptance Criteria
- [ ] Displays Title and Artist in stage header during playback.
- [ ] Displays total duration and real-time remaining countdown `(-MM:SS)`.
- [ ] Smoothly cross-fades between "Now Singing" and "Up Next" when queue is non-empty.
- [ ] Resets immediately to "Now Singing" when queue becomes empty or playback changes.

## Blocked by
- None (can start immediately)
