---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: in-review
---

# STORY-0010: Dynamic Karaoke Stage Header, Countdown Cues & Customization Controls

## Parent Epic
- `docs/tickets/EPIC-0003-karaoke-metadata-and-stage-enhancements.md`

## What it delivers
Transforms the Karaoke Stage with a dynamic alternating stage header ("Now Singing: [Title] • [Artist]" ⟷ "Up Next: [Next Title] • [Next Artist]") with real-time remaining time countdown, visual 3-beat countdown cues before singing starts, and user-configurable stage settings (font resizing `A-`/`A+`, transition interval, and active glow colors) persisted in `localStorage`.

## Acceptance Criteria
- [x] Karaoke stage header displays Title, Artist, total time, and remaining time countdown badge.
- [x] When upcoming queued songs exist, header smoothly cross-fades between "Now Singing" and "Up Next" on a configurable interval (default 6s).
- [x] Visual countdown cue (`● ○ ○` -> `● ● ○` -> `● ● ●`) pulses 3 seconds prior to the first lyric line and after instrumental interludes > 5s.
- [x] Users can scale lyric font size dynamically via `A-` / `A+` buttons on the stage toolbar.
- [x] Stage Settings modal allows adjusting transition interval, highlight color, and base font size with persistent `localStorage` storage.

## Tasks
- [x] TASK-0023: Alternating "Now Singing" ⟷ "Up Next" Header & Remaining Time Badge
- [x] TASK-0024: Visual Intro & Interlude 3-Beat Countdown Cue Engine
- [x] TASK-0025: Stage Toolbar Lyric Resizing (A-/A+) & Configurable Settings Modal

## Blocked by
- None (can start immediately in parallel)

