---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# STORY-0020: Expanded Studio Song Catalog Modal & Default Recent Sort

## Parent Epic
- `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

## What it delivers
Provides a full-screen expanded song catalog modal in Stem Studio with search, 4-way sorting, and direct `📝 Edit Details / Lyrics` access, and sets the default Studio Library sort order to Recently Added.

## Acceptance Criteria
- [x] Clicking `⛶` in Studio Song Library header opens `#studio-catalog-modal` with search, sorting, and editing actions.
- [x] Studio Song Library defaults to descending `created_at` sort order.

## Tasks
- [x] TASK-0046: Expanded Studio Song Catalog Modal with Search, Sort & Lyric Editing
- [x] TASK-0047: Studio Song Library Default "Recently Added" Sort Order

## Implementation
- Branch: `story/STORY-0020-studio-catalog-and-recent-sort`
- Completed TASK-0046 and TASK-0047, verified by 97 passing automated tests.

## Blocked by
- `docs/tickets/STORY-0019-collapsible-accordions-and-notes-modal.md` (in-review)
