---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: in-review
---

# STORY-0023: Interactive 1-Click LRCLIB Lyrics Auto-Fetch in Lyrics Modal

## Parent Epic
- `docs/tickets/EPIC-0007-lrclib-lyrics-integration.md`

## What it delivers
Provides a 1-click `⚡ Auto-Fetch LRC` action inside the Song Details & Lyrics editor modal (`#lyrics-modal`) allowing users to query LRCLIB on-demand using current Title/Artist input fields, with real-time feedback and direct preview.

## Acceptance Criteria
- [x] `#fetch-lrclib-btn` in `#lyrics-modal` triggers `/api/lyrics/lrclib/get` using modal input values.
- [x] Populates `#lyrics-textarea` with retrieved timestamped `.lrc` lyrics upon success.
- [x] Displays clear inline status alerts for loading, success, and no-match/error states.
- [x] Allows editing and saving lyrics seamlessly.

## Tasks
- [x] TASK-0053: Interactive Lyrics Modal Auto-Fetch UI & Inline Feedback

## Implementation
- Added `⚡ Auto-Fetch LRC` button in `#lyrics-modal` in `src/static/index.html`.
- Implemented real-time retrieval with inline status banners in `src/static/library_queue.js`.
- Verified in `tests/test_lyrics_modal_frontend.py`.

## Blocked by
- `docs/tickets/STORY-0022-lrclib-client-and-pipeline-auto-sync.md`
