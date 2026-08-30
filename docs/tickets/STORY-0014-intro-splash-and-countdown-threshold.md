---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# STORY-0014: Title/Artist Intro Splash Screen & Configurable Gap Countdown Cue Engine

## Parent Epic
- `docs/tickets/EPIC-0005-karaoke-stage-ux-and-song-catalog.md`

## What it delivers
Provides performers with adequate visual preparation time by presenting a prominent Song Title and Artist splash screen overlay on the lyrics stage with delayed audio start (0–5s, configurable in Stage Settings), and enhances the visual countdown cue engine with a configurable non-lyric gap threshold (3–5s, default 3s) for accurate cues during intros and instrumental interludes.

## Acceptance Criteria
- [ ] Song load triggers an animated Title & Artist splash overlay on the lyrics stage for the duration set in Stage Settings (0–5s, default 3s).
- [ ] Multitrack audio stems pre-buffer during the splash and playback start is delayed by precisely the splash duration (0s starts immediately).
- [ ] Stage Settings includes an "Intro Splash Duration" slider (0s–5s).
- [ ] Stage Settings includes a "Countdown Cue Threshold" slider (3s–5s, default 3s).
- [ ] Visual 3-beat countdown cues (● ○ ○ → ● ● ○ → ● ● ●) trigger exactly 3.0s prior to singing when intro or instrumental gap >= configured threshold.

## Tasks
- [ ] TASK-0033: Title & Artist Intro Splash Overlay with Pre-buffered Audio Delay (0–5s)
- [ ] TASK-0034: Configurable Countdown Cue Gap Threshold (3s–5s) & Instrumental Interlude Evaluator

## Blocked by
- None (can start immediately)
