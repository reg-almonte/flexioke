---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: pending
---

# STORY-0026: Smart Idle Stage Play Dispatch & Catalog Fallback

## Parent Epic
- `docs/tickets/EPIC-0008-lyrics-calibration-and-karaoke-ux.md`

## What it delivers
Enhances the primary transport Play button and stage canvas click when the stage is idle (`currentJob == null`) to automatically dequeue and play the first song in the queue, or open the Song Catalog modal if the queue is empty.

## Acceptance Criteria
- [ ] Clicking Play or stage canvas on an idle stage starts playing the first queued track when queue is non-empty.
- [ ] Clicking Play or stage canvas on an idle stage opens `#song-catalog-modal` when queue is empty.
- [ ] Normal play/pause toggling remains unaffected when a track is actively loaded.

## Tasks
- [ ] TASK-0056: Empty Stage Play Transport Queue Dispatch & Catalog Modal Fallback
