---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# Version 0.2.6: Synchronized Lyrics Calibration & Karaoke UX Enhancements — Check Sheet

## Related
- Functional spec: `docs/specs/version0.2.6.md`
- ADR: `docs/design/ADR-0009-lyrics-calibration-and-karaoke-ux.md`
- Epic: `docs/tickets/EPIC-0008-lyrics-calibration-and-karaoke-ux.md`
- Stories: `docs/tickets/STORY-0024-lyrics-modal-timestamp-calibration.md`, `docs/tickets/STORY-0025-karaoke-sidebar-accordions.md`, `docs/tickets/STORY-0026-smart-idle-stage-play-dispatch.md`
- Tasks: `docs/tickets/TASK-0054-lrc-timestamp-shift-parser-and-toolbar.md`, `docs/tickets/TASK-0055-karaoke-sidebar-accordions-and-persistence.md`, `docs/tickets/TASK-0056-empty-stage-play-dispatch-and-fallback.md`

## Verification Items

### 1. In-Modal LRC Timestamp Calibration Toolbar (STORY-0024 / TASK-0054)
- [x] `#lyrics-modal` contains calibration toolbar with quick buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`), custom delta input `#lyrics-custom-shift-input`, and `#lyrics-shift-alert` — verified by: `tests/test_v026_features.py::test_lyrics_calibration_toolbar_dom_elements` & `tests/test_lyrics_modal_frontend.py`
- [x] `shiftLrcTimestamps` supports both 2-decimal and 3-decimal regex patterns (`\[\d{2}:\d{2}(?:\.\d{1,3})?\]`) — verified by: `tests/test_v026_features.py::test_lrc_timestamp_shifting_algorithm`
- [x] Positive offset calculation shifts all timestamp lines accurately and rollover minutes correctly — verified by: `tests/test_v026_features.py::test_lrc_timestamp_shifting_algorithm`
- [x] Negative offset calculation clamps to minimum `[00:00.00]` without producing negative timestamps — verified by: `tests/test_v026_features.py::test_lrc_timestamp_shifting_algorithm`
- [x] Metadata headers (`[ti:...]`, `[ar:...]`), empty lines, and untimed text are preserved unaltered — verified by: `tests/test_v026_features.py::test_lrc_timestamp_shifting_algorithm`
- [x] Calibration toolbar modifies `#lyrics-textarea` in-place without triggering server round-trips before saving — verified by: `tests/test_lyrics_modal_frontend.py`
- [x] Auto-dismissing feedback badge displays updated line count and delta for 2.5s — verified by: `tests/test_lyrics_modal_frontend.py`
- [ ] User clicks quick shift buttons and custom shift input to adjust lyrics and saves permanently via `POST /api/jobs/{id}/lyrics` — verified by: manual test in browser

### 2. Collapsible Karaoke Sidebar Accordions (STORY-0025 / TASK-0055)
- [x] Playback Queue accordion container `#accordion-header-karaoke-queue`, body `#accordion-body-karaoke-queue`, and chevron `#accordion-chevron-karaoke-queue` present in `#view-karaoke` — verified by: `tests/test_v026_features.py::test_karaoke_sidebar_accordions_dom_and_attributes`
- [x] Song Library accordion container `#accordion-header-karaoke-library`, body `#accordion-body-karaoke-library`, and chevron `#accordion-chevron-karaoke-library` present in `#view-karaoke` — verified by: `tests/test_v026_features.py::test_karaoke_sidebar_accordions_dom_and_attributes`
- [x] Headers have accessible attributes `role="button"` and `tabindex="0"` — verified by: `tests/test_v026_features.py::test_karaoke_sidebar_accordions_dom_and_attributes`
- [x] Accordion toggle logic updates chevron indicator rotation and manages `.hidden` body state — verified by: `tests/test_library_queue_frontend.py::test_karaoke_sidebar_accordions`
- [x] Accordion open/collapsed state persists to `localStorage['flexioke_karaoke_accordions']` across page reloads and tab switches — verified by: `tests/test_library_queue_frontend.py::test_karaoke_sidebar_accordions`
- [ ] User clicks accordion headers or presses Enter/Space to collapse and expand cards with smooth UI chevron transitions — verified by: manual test in browser

### 3. Smart Idle Stage Play Action & Empty Queue Fallback (STORY-0026 / TASK-0056)
- [x] Transport play button `#karaoke-play-btn` and idle stage background `#karaoke-lyrics-stage` dispatch smart play when `currentJob == null` — verified by: `tests/test_karaoke_controls_and_interruption.py::test_karaoke_idle_stage_smart_play_dispatch` & `tests/test_v026_features.py::test_karaoke_smart_idle_play_dispatch_wiring`
- [x] Smart play loads and starts the top song via `window.flexiokeQueue.playNext()` / `advanceNext(true)` when queue has $\ge 1$ songs — verified by: `tests/test_karaoke_controls_and_interruption.py::test_karaoke_idle_stage_smart_play_dispatch`
- [x] Smart play falls back to opening `#song-catalog-modal` with search focused when queue is empty — verified by: `tests/test_karaoke_controls_and_interruption.py::test_karaoke_idle_stage_smart_play_dispatch`
- [x] `window.flexiokeSongLibrary` alias maintained on `window.flexiokeLibrary` for backwards compatibility — verified by: `tests/test_karaoke_controls_and_interruption.py::test_karaoke_idle_stage_smart_play_dispatch`
- [ ] User presses Space or clicks stage when idle with queued songs to start playback immediately — verified by: manual test in browser
- [ ] User presses Space or clicks stage when idle with empty queue to open song catalog modal — verified by: manual test in browser

## Completeness Review (auto-generated)

- **Review Date:** 2026-09-05
- **Reviewed Against:**
  - Functional Spec: `docs/specs/version0.2.6.md`
  - ADR: `docs/design/ADR-0009-lyrics-calibration-and-karaoke-ux.md`
  - Tickets: `docs/tickets/EPIC-0008-lyrics-calibration-and-karaoke-ux.md`, `STORY-0024`, `STORY-0025`, `STORY-0026`, `TASK-0054`, `TASK-0055`, `TASK-0056`
- **Result:** No gaps found. Full 1:1 bidirectional mapping across all 3 functional flows, edge cases, DOM components, accessibility attributes, persistence behaviors, and test suites.
- **Missing Coverage:** None.
- **Orphaned Entries:** None.

## Test Execution — 2026-09-06

- **Test Suite Result:** 117 passed, 0 failed in 4.06s (100% pass rate).
- **Automated Verification Items:** 16/16 verified and passing.
- **Manual Verification Items:** 4 items designated for human browser confirmation.
- **Defects / Bug Reports:** 0 bugs filed. Status is clean.
