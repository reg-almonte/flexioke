---
status: fixed
filed_at: 2026-09-07
verified_at: 2026-09-10
---


# Bug Report: Button Click Event Propagation on Karaoke Stage

## Related
- Functional Spec: `docs/specs/version0.3.1.md` (§3 YouTube-Style Fullscreen Cinema Stage)
- Design: `docs/design/ADR-0011-ui-and-stage-experience-enhancements.md` (§3 Floating Chrome & Fullscreen)
- Story: `docs/tickets/archive/v0.3.1/STORY-0033-youtube-style-fullscreen-karaoke-stage.md`
- Tasks: `docs/tickets/archive/v0.3.1/TASK-0069-cinema-fullscreen-floating-chrome.md`, `docs/tickets/archive/v0.3.1/TASK-0070-inactivity-autohide-and-stage-shortcuts.md`

## Summary
When clicking interactive buttons inside `#karaoke-stage-card` (such as `#karaoke-fullscreen-btn`, `#karaoke-exit-fullscreen-btn`, transport buttons, vocal toggles, or settings buttons), the click event bubbles up to the stage card container (`#karaoke-stage-card`), inadvertently triggering the background click-to-play/pause handler. This causes songs to unintentionally play or pause when entering/exiting fullscreen or toggling controls.

## Failures & Root Cause Analysis

### Failure 1: Unhandled Click Event Bubbling on Stage Control Buttons
- **Root Cause:**
  1. In `src/static/karaoke.js`, button click listeners (such as `this.fullscreenBtn.addEventListener('click', ...)`, `this.exitFullscreenBtn`, `this.playBtn`, `this.restartBtn`, `this.skipBtn`, `this.stopBtn`, `this.settingsBtn`, `this.toggleLeadBtn`, and `this.toggleBackingBtn`) did not invoke `e.stopPropagation()`.
  2. When `#karaoke-fullscreen-btn` is clicked, `toggleFullscreen()` executes synchronously, immediately replacing `this.fullscreenIcon.innerHTML`. This DOM replacement detaches the clicked `<svg>`/`<path>` element from the active DOM tree.
  3. When the event bubbles to `stageTarget` (`#karaoke-stage-card`), the container's guard `if (e.target.closest('button, ...'))` evaluates on the detached element and returns `null` because the detached element is no longer part of the button DOM tree.
  4. Consequently, `stageTarget`'s click listener falls through and executes `this.togglePlayPause()`.
- **Proposed Fix:**
  1. Add `e.stopPropagation()` to all button click listeners in `src/static/karaoke.js` (`this.fullscreenBtn`, `this.exitFullscreenBtn`, `this.playBtn`, `this.restartBtn`, `this.skipBtn`, `this.stopBtn`, `this.settingsBtn`, `this.closeSettingsModalBtn`, `this.saveSettingsBtn`, `this.resetSettingsBtn`, `this.timecodeEl`, `this.toggleLeadBtn`, `this.toggleBackingBtn`, `this.volumeSlider`).
  2. Add `click` and `dblclick` event isolation (`e.stopPropagation()`) directly to `#karaoke-top-header`, `#karaoke-transport-bar`, `#karaoke-settings-modal`, `#karaoke-intro-splash`, and `#karaoke-countdown-cue` containers.
  3. Strengthen the `e.target.closest('button, input, textarea, a, select, label, ...')` guard in `stageTarget`'s `click` and `dblclick` handlers.
  4. Add automated unit and Node.js regression tests in `tests/test_karaoke_cinema_fullscreen.py`.

## Applied Fixes (Pending Phase 6 Verification)
1. **Button & Control Event Isolation:**
   - Added `e.stopPropagation()` to `fullscreenBtn`, `exitFullscreenBtn`, `playBtn`, `restartBtn`, `skipBtn`, `stopBtn`, `settingsBtn`, `closeSettingsModalBtn`, `saveSettingsBtn`, `resetSettingsBtn`, `timecodeEl`, `toggleLeadBtn`, `toggleBackingBtn`, and `volumeSlider` in `src/static/karaoke.js`.
2. **Container Overlays Isolation:**
   - Added `click` and `dblclick` stopPropagation handlers to `topHeaderEl`, `transportBarEl`, `settingsModal`, `introSplash`, and `countdownCue`.
3. **Stage Click Guard Expansion:**
   - Expanded the `e.target.closest(...)` selector in `stageTarget` click & dblclick listeners to guard against all interactive and overlay elements (`button, input, textarea, a, select, label, .karaoke-line, #karaoke-top-header, #karaoke-transport-bar, #karaoke-settings-modal, #karaoke-intro-splash, #karaoke-countdown-cue`).
4. **Automated Testing:**
   - Added `test_stage_buttons_stop_event_propagation` in `tests/test_karaoke_cinema_fullscreen.py` including Node.js event bubbling isolation simulation. Verified 162/162 passing tests.

