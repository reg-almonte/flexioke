---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: pending
---

# TASK-0056: Empty Stage Play Transport Queue Dispatch & Catalog Modal Fallback

## Parent Story
- `docs/tickets/STORY-0026-smart-idle-stage-play-dispatch.md`

## What to build
1. In `KaraokeStageManager.handlePlayPause()` in `src/static/karaoke_stage.js`:
   - If `!this.currentJob`:
     - If `window.flexiokeQueue && window.flexiokeQueue.queue.length > 0`: invoke `window.flexiokeQueue.playNext()`.
     - Else: invoke `window.flexiokeSongLibrary.openCatalogModal()`.
2. In stage canvas click handler in `src/static/karaoke_stage.js`:
   - If `!this.currentJob`, apply the same smart queue dispatch / catalog fallback.
3. Add automated tests in `tests/test_karaoke_controls_and_interruption.py` or `tests/test_karaoke_navigation.py`.

## Acceptance Criteria
- [ ] Primary Play button on idle stage triggers `playNext()` from non-empty queue.
- [ ] Primary Play button on idle stage with empty queue opens `#song-catalog-modal`.
- [ ] Stage background click on idle stage triggers the same dispatch/fallback.
