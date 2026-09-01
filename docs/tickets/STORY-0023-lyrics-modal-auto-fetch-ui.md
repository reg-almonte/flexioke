---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: pending
---

# STORY-0023: Interactive 1-Click LRCLIB Lyrics Auto-Fetch in Lyrics Modal

## Parent Epic
- `docs/tickets/EPIC-0007-lrclib-lyrics-integration.md`

## What it delivers
Provides a 1-click `⚡ Auto-Fetch LRC` action inside the Song Details & Lyrics editor modal (`#lyrics-modal`) allowing users to query LRCLIB on-demand using current Title/Artist input fields, with real-time feedback and direct preview.

## Acceptance Criteria
- [ ] `#fetch-lrclib-btn` in `#lyrics-modal` triggers `/api/lyrics/lrclib/get` using modal input values.
- [ ] Populates `#lyrics-textarea` with retrieved timestamped `.lrc` lyrics upon success.
- [ ] Displays clear inline status alerts for loading, success, and no-match/error states.
- [ ] Allows editing and saving lyrics seamlessly.

## Tasks
- [ ] TASK-0053: Interactive Lyrics Modal Auto-Fetch UI & Inline Feedback

## Blocked by
- `docs/tickets/STORY-0022-lrclib-client-and-pipeline-auto-sync.md`
