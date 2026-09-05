---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: in-review
---

# TASK-0055: Karaoke Sidebar Accordions & LocalStorage Persistence

## Parent Story
- `docs/tickets/STORY-0025-karaoke-sidebar-accordions.md`

## What to build
1. In `src/static/index.html`, restructure `#karaoke-card-queue` and `#karaoke-card-library` with header toggle buttons (`#karaoke-queue-header-btn`, `#karaoke-library-header-btn`), animated chevrons, and content wrappers (`#karaoke-queue-content`, `#karaoke-library-content`).
2. In `src/static/karaoke.js`, implement accordion toggle listeners and `localStorage` state loading/saving.
3. Add automated tests in `tests/test_library_queue_frontend.py`.

## Acceptance Criteria
- [x] Clicking headers toggles visibility of queue and library cards.
- [x] Chevrons rotate when collapsed.
- [x] Saved states in `localStorage` restore correctly on initialization.

## Implementation
- Restructured Karaoke cards in `src/static/index.html` with accordion headers, chevrons, and content wrappers.
- Implemented `initKaraokeAccordions()` in `src/static/karaoke.js` with `localStorage['flexioke_karaoke_accordions']` caching.
- Verified in `tests/test_library_queue_frontend.py`.
