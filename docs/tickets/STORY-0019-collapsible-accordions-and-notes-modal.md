---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# STORY-0019: Stem Studio Collapsible Accordions & Persistent Notes Scratchpad

## Parent Epic
- `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

## What it delivers
Provides collapsible accordion cards in the Stem Studio sidebar to conserve vertical screen space, and adds a persistent notes scratchpad modal in the header for resource links and bookmarks.

## Acceptance Criteria
- [x] Sidebar cards ("Add Song", "Studio Song Library", "Studio Queue") collapse and expand with smooth chevrons and remember state in `localStorage`.
- [x] Header `📝 Notes` button opens `#studio-notes-modal` with real-time auto-saving and clickable link detection.

## Tasks
- [x] TASK-0044: Collapsible Sidebar Accordions with LocalStorage State
- [x] TASK-0045: Persistent Header Notes / Resource Links Scratchpad Modal

## Implementation
- Branch: `story/STORY-0019-stem-studio-accordions-and-notes`
- Completed TASK-0044 and TASK-0045, verified by 96 passing automated tests.

## Blocked by
- `docs/tickets/STORY-0018-multi-upload-and-fifo-separation-queue.md` (in-review)
