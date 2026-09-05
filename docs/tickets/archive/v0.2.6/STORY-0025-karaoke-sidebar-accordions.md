---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: in-review
---

# STORY-0025: Collapsible Sidebar Accordions in Karaoke Mode

## Parent Epic
- `docs/tickets/EPIC-0008-lyrics-calibration-and-karaoke-ux.md`

## What it delivers
Provides collapsible accordion headers for the Playback Queue and Song Library sidebar cards in Karaoke Mode (`#view-karaoke`) with smooth chevron animations and localStorage persistence.

## Acceptance Criteria
- [x] Playback Queue card can be collapsed and expanded.
- [x] Song Library card can be collapsed and expanded.
- [x] Chevron rotates 180 degrees when collapsed.
- [x] Accordion states persist in `localStorage['flexioke_karaoke_accordions']` across page refreshes.

## Tasks
- [x] TASK-0055: Karaoke Sidebar Accordions & LocalStorage Persistence

## Implementation
- Restructured Karaoke cards in `src/static/index.html`.
- Implemented `initKaraokeAccordions()` in `src/static/karaoke.js`.
- Verified in `tests/test_library_queue_frontend.py`.
