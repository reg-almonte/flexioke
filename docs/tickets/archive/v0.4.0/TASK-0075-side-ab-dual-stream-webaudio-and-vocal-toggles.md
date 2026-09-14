---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: in-review
---

# TASK-0075: Dual-Stream WebAudio Hot-Swapping & Dynamic Vocal Toggles

## Parent Story
- `docs/tickets/STORY-0036-side-ab-dual-track-ingestion-and-playback.md`

## What to build
Build the audio playback coordination and dynamic vocal toggle state adapter for Side A/B tracks:
- Preload and timecode-lock both Side B (`instrumental`) and Side A (`lead_vocals`) in player engine.
- Upon clicking `#karaoke-toggle-lead-btn` during a Side A/B song:
  - Lead Vocal ON: Set Side A gain to master volume; mute Side B (gain = 0).
  - Lead Vocal OFF: Set Side B gain to master volume; mute Side A (gain = 0).
- Dynamically adapt vocal toggle button states:
  - If only Side B exists: disable `#karaoke-toggle-lead-btn` with text `Lead: OFF (Side B Only)`.
  - If only Side A exists: disable `#karaoke-toggle-lead-btn` with text `Lead: ON (Side A Only)`.
  - Disable Backing Vocal button with text `Backing: N/A (Side A/B)`.
- Render `Side A/B` badges in Song Library, Playlists, and Song Catalog modal.

## Acceptance Criteria
- [x] Lead Vocal button hot-swaps between Side A and Side B with zero delay or drift.
- [x] Single-sided tracks disable the Lead Vocal button in the appropriate state.
- [x] Backing Vocal button is locked to disabled state for all Side A/B songs.
- [x] Automated frontend player and Node.js regression tests pass cleanly.

## Blocked by
- `TASK-0074`
