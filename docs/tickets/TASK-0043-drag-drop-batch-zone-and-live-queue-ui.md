---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0043: Multi-File Drag-and-Drop Batch Dropzone & Live Queue Progress UI

## Parent Story
- `docs/tickets/STORY-0018-multi-upload-and-fifo-separation-queue.md`

## What to build
Implement HTML5 drag-and-drop batch upload dropzone (`#studio-dropzone`) and multi-file input (`<input type="file" multiple accept="audio/*">`) in Stem Studio. Render active and queued jobs in `#processing-queue-container` with progress bars, position badges (`Position #2 in queue`), and cancel buttons.

## Acceptance Criteria
- [ ] Drag-and-drop zone accepts single or multiple audio files with hover feedback.
- [ ] Live queue list renders all queued jobs with position badges.
- [ ] Clicking cancel button dispatches cancellation request and updates UI.

## Blocked by
- TASK-0042: In-Process Thread-Safe FIFO Separation Worker & Queue Cancellation
