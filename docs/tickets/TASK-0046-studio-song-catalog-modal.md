---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0046: Expanded Studio Song Catalog Modal with Search, Sort & Lyric Editing

## Parent Story
- `docs/tickets/STORY-0020-studio-catalog-modal-and-default-sort.md`

## What to build
Add Expand button (`#open-studio-catalog-btn`, icon `⛶`) to Studio Song Library header and build `#studio-catalog-modal` with real-time search, clear (`✕`), 4-way sort selector (`Recently Added`, `Title A-Z/Z-A`, `Artist A-Z`), and `▶ Play Now`, `➕ Queue`, and `📝 Edit Details / Lyrics` actions on each card.

## Acceptance Criteria
- [x] Modal opens and displays full list of songs with search and sorting.
- [x] Cards include `▶ Play Now`, `➕ Add to Queue`, and `📝 Edit Details / Lyrics`.
- [x] Modal closes cleanly via `Esc`, close button, or backdrop click.

## Implementation
- Added `#open-studio-catalog-btn` to Studio Library header in `src/static/index.html`.
- Bound catalog modal trigger and added `📝 Edit` button on each catalog card opening the lyrics & metadata modal in `src/static/library_queue.js`.
- Verified in `tests/test_library_queue_frontend.py`.

## Blocked by
- None (can start immediately)
