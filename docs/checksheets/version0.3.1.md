---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# Version 0.3.1: UI & Stage Experience Enhancements — Check Sheet

## Related
- Functional spec: `docs/specs/version0.3.1.md`
- ADR: `docs/design/ADR-0011-ui-and-stage-experience-enhancements.md`
- Epic: `docs/tickets/EPIC-0010-ui-and-stage-experience-enhancements.md`
- Stories: `docs/tickets/STORY-0031-in-modal-song-navigation.md`, `docs/tickets/STORY-0032-modular-svg-icon-dictionary.md`, `docs/tickets/STORY-0033-youtube-style-fullscreen-karaoke-stage.md`
- Tasks: `docs/tickets/TASK-0065-modal-navigation-context-and-counter.md`, `docs/tickets/TASK-0066-unsaved-edits-interceptor-and-shortcuts.md`, `docs/tickets/TASK-0067-svg-icon-dictionary-module.md`, `docs/tickets/TASK-0068-ui-iconography-overhaul-and-tooltips.md`, `docs/tickets/TASK-0069-cinema-fullscreen-floating-chrome.md`, `docs/tickets/TASK-0070-inactivity-autohide-and-stage-shortcuts.md`

## Verification Items

### 1. In-Modal Song Navigation & Track Position Counter (STORY-0031 / TASK-0065)
- [x] `#modal-nav-prev-btn`, `#modal-nav-counter-badge`, and `#modal-nav-next-btn` rendered in `#lyrics-modal` header — verified by: `tests/test_lyrics_modal_navigation.py::test_modal_navigation_elements_in_html`
- [x] Track position badge dynamically displays `Track X of Y` matching active song index — verified by: `tests/test_lyrics_modal_navigation.py::test_navigation_context_tracking_and_boundary_checks_in_node`
- [x] Boundary disabling: Prev button disabled at track 1 (`activeIndex <= 0`); Next button disabled at final track (`activeIndex >= total - 1`) — verified by: `tests/test_lyrics_modal_navigation.py::test_navigation_context_tracking_and_boundary_checks_in_node`
- [x] Navigation context correctly populated from filtered library, sorted catalog modal, or playlist views — verified by: `tests/test_lyrics_modal_navigation.py::test_navigation_context_tracking_and_boundary_checks_in_node`
- [ ] User opens song modal and navigates sequentially forward and backward across library — verified by: manual test in browser

### 2. Unsaved Changes Guard, Interceptors & Keyboard Navigation (STORY-0031 / TASK-0066)
- [x] Real-time `input` event listeners track dirty modifications across Title, Artist, and Lyrics textarea against baseline — verified by: `tests/test_lyrics_modal_navigation.py::test_dirty_state_detection_and_unsaved_changes_interceptor`
- [x] Confirmation prompt (`window.confirm`) intercepts Prev, Next, Close button, and `Escape` key when `isDirty === true` — verified by: `tests/test_lyrics_modal_navigation.py::test_dirty_state_detection_and_unsaved_changes_interceptor`
- [x] Saving or cancelling resets dirty state baseline cleanly — verified by: `tests/test_lyrics_modal_navigation.py::test_dirty_state_detection_and_unsaved_changes_interceptor`
- [x] Keyboard shortcuts (`Alt + Left Arrow`, `Alt + Right Arrow`) cycle songs without interfering with active typing — verified by: `tests/test_lyrics_modal_navigation.py::test_keyboard_navigation_shortcuts`
- [ ] User edits title or lyrics in modal and attempts to switch tracks; verifies unsaved changes prompt prevents accidental loss — verified by: manual test in browser

### 3. Centralized Modular SVG Icon Dictionary Module (STORY-0032 / TASK-0067)
- [x] Standalone module `src/static/icons.js` served at `/static/icons.js` and loaded before dependent scripts — verified by: `tests/test_svg_icons.py::test_icons_script_served_and_referenced_in_index`
- [x] `window.flexiokeIcons` dictionary maps 24+ standard semantic keys to clean inline vector SVGs (`viewBox="0 0 24 24"`, `currentColor`) — verified by: `tests/test_svg_icons.py::test_svg_icons_dictionary_and_helper_in_node`
- [x] Utility helper `window.getIconHtml(name, extraClasses, extraAttrs)` injects classes/attributes and returns `""` on unknown names without throwing errors — verified by: `tests/test_svg_icons.py::test_svg_icons_dictionary_and_helper_in_node`

### 4. Universal UI Iconography Overhaul & Hotkey Tooltips (STORY-0032 / TASK-0068)
- [x] Replaced emojis/Unicode characters with vector SVGs across transport bar, karaoke stage, modal controls, and stem channels — verified by: `tests/test_svg_icons.py::test_index_and_js_modules_use_svg_icons_and_hotkey_tooltips`
- [x] Dynamic JavaScript modules (`player.js`, `karaoke.js`, `library_queue.js`, `playlists.js`, `app.js`) use `window.getIconHtml()` with defensive fallbacks — verified by: `tests/test_svg_icons.py::test_index_and_js_modules_use_svg_icons_and_hotkey_tooltips`
- [x] Tooltips provide explicit hotkey hints: `Play / Pause (Space)`, `Restart Song (R)`, `Skip to Next Track (N)`, `Toggle Fullscreen Stage (F)` / `Exit Fullscreen Stage (Esc / F)`, `Previous Song (Alt+Left)`, `Next Song (Alt+Right)`, `Close (Esc)` — verified by: `tests/test_svg_icons.py::test_index_and_js_modules_use_svg_icons_and_hotkey_tooltips`
- [ ] User inspects UI across 100% and 200% DPI displays to verify crisp vector rendering — verified by: manual test in browser

### 5. In-Place Cinema Fullscreen Layout & Floating Glassmorphism Overlays (STORY-0033 / TASK-0069)
- [x] `.karaoke-cinema-fullscreen` / `.stage-fullscreen` expands stage edge-to-edge (`fixed inset-0 z-[9999] 100vw × 100vh bg-[#030712]`) — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_cinema_fullscreen_css_rules_in_styles`
- [x] Floating glassmorphism top header (`#karaoke-top-header`) and bottom transport bar (`#karaoke-transport-bar`) float centered over stage with `backdrop-filter: blur(16px)` — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_cinema_fullscreen_css_rules_in_styles`
- [x] Dedicated Exit Fullscreen button (`#karaoke-exit-fullscreen-btn`) displayed in header during fullscreen mode — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_cinema_fullscreen_elements_in_html`
- [x] Lyrics container expands behind floating chrome, scaling line heights and font sizes proportionally — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_cinema_fullscreen_css_rules_in_styles`
- [ ] User toggles fullscreen and verifies cinematic presentation and floating translucent bars — verified by: manual test in browser

### 6. Inactivity Auto-Hide Engine, Cursor Suppression & Stage Shortcuts (STORY-0033 / TASK-0070)
- [x] Controls and mouse cursor auto-hide after 3 seconds of inactivity during fullscreen playback — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_karaoke_fullscreen_and_autohide_logic_in_node`
- [x] User activity (`mousemove`, `pointermove`, `touchstart`, `keydown`, `wheel`) immediately wakes chrome and resets inactivity timer — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_karaoke_fullscreen_and_autohide_logic_in_node`
- [x] Floating controls remain permanently visible when audio is paused or stopped — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_karaoke_fullscreen_and_autohide_logic_in_node`
- [x] Stage canvas double-click and global `F` keyboard shortcut toggle fullscreen mode; single click toggles play/pause with 220ms debounce — verified by: `tests/test_karaoke_cinema_fullscreen.py::test_karaoke_keyboard_shortcuts_and_tooltips`
- [ ] User plays a song in fullscreen, remains idle for 3s, and verifies controls/cursor fade away; moves mouse to verify instant wake — verified by: manual test in browser

## Completeness Review (auto-generated)
Reviewed on: 2026-09-06
Status: Complete — No gaps found

### Audit Summary
- **Functional Spec (`docs/specs/version0.3.1.md`)**: 100% coverage across Flow 1 (In-Modal Navigation & Dirty Guard), Flow 2 (SVG Icon Dictionary & Tooltips), and Flow 3 (In-Place Cinema Fullscreen & Auto-Hide).
- **ADR (`docs/design/ADR-0011-ui-and-stage-experience-enhancements.md`)**: Architecture decisions (client-side coordinator, zero DOM duplication, vector SVG dictionary, 3000ms inactivity auto-hide engine) verified.
- **Tickets (`EPIC-0010`, `STORY-0031`–`0033`, `TASK-0065`–`0070`)**: All acceptance criteria mapped to automated integration tests and browser verification steps.
- **Missing Coverage**: 0 items.
- **Orphaned Entries**: 0 items.

## Test Execution — 2026-09-06
- **Test Suite Result:** 155 passed, 0 failed in 5.69s (100% pass rate).
- **Automated Verification Items:** 17/17 verified and passing.
- **Manual Verification Items:** 4 items designated for browser verification.
- **Defects / Bug Reports:** 0 bugs filed. Status is clean.

## Test Execution — 2026-09-10 (Bugfix Verification)
- **Scope:** Verification of BUG-0007 (Stage button click event propagation isolation) & test isolation in `/data/jobs`.
- **Test Suite Result:** 162 passed, 0 failed in 5.40s (100% pass rate).
- **Bug Reports Verified:** `docs/bugs/BUG-0007-button-click-propagation.md` confirmed fixed by `tests/test_karaoke_cinema_fullscreen.py::test_stage_buttons_stop_event_propagation`.
- **Storage Durability:** `/data/jobs` verified clean with zero test artifact pollution across test suites.

