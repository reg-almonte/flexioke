---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: pending
---

# TASK-0053: Interactive Lyrics Modal Auto-Fetch UI & Inline Feedback

## Parent Story
- `docs/tickets/STORY-0023-lyrics-modal-auto-fetch-ui.md`

## What to build
Add a `⚡ Auto-Fetch LRC` button in `#lyrics-modal` in `src/static/index.html`. In `src/static/library_queue.js`, wire the button to query `/api/lyrics/lrclib/get` with current Title and Artist inputs, load the returned lyrics into `#lyrics-textarea`, and show clear inline feedback alerts.

## Acceptance Criteria
- [ ] `#fetch-lrclib-btn` queries backend proxy and populates `#lyrics-textarea` with `.lrc` lyrics.
- [ ] Displays loading state during request and inline alert upon success or failure.
- [ ] User can edit the fetched text and save normally.

## Blocked by
- `docs/tickets/TASK-0051-lrclib-client-module-and-proxy-endpoints.md`
