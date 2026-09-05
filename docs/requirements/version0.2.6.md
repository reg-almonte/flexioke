---
status: approved
approved_by: reg
approved_at: 2026-09-05
---

# Version 0.2.6: Synchronized Lyrics Calibration & Karaoke UX Enhancements

## Problem / Motivation
1. **LRC Timing Mismatches:** Synchronized `.lrc` lyrics from online databases or manual transcription may lead or lag behind the vocals by a fraction of a second due to differing master tracks or intro silence. Currently, users must manually rewrite every single timestamp line-by-line.
2. **Karaoke Sidebar Clutter:** In Karaoke Mode, the Playback Queue and Song Library cards are fixed in size and cannot be minimized to reduce screen distraction when singers want a cleaner interface.
3. **Idle Stage Play Button Dead End:** When no track is active, pressing the transport Play button (`▶`) or clicking the stage does nothing, even when songs are waiting in the Playback Queue or when the user wants to browse the library.

## Target Users
- **Karaoke Singers & Party Hosts:** Need quick lyric calibration for out-of-sync songs and streamlined one-touch playback from the queue.
- **Stem Studio Users:** Want instant global calibration tools to fine-tune `.lrc` files directly in the editor.

## Goals
1. **Frontend Global & Directional LRC Time-Shift Tool:** Provide quick 1-click buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`) and custom offset input in `#lyrics-modal` that instantly recalculates all `[MM:SS.xx]` timestamps in place with minimum `00:00.00` clamping.
2. **Collapsible Sidebar Accordions in Karaoke Mode:** Allow users to collapse/expand the Playback Queue and Song Library sidebars in Karaoke Mode with smooth animations and `localStorage` persistence, consistent with Stem Studio.
3. **Smart Play from Queue & Catalog Fallback:**
   - If no song is loaded/playing and the Playback Queue has songs: pressing the primary Play button or clicking the idle stage automatically loads and starts the first queued track.
   - If no song is loaded/playing and the Playback Queue is empty: pressing the primary Play button or clicking the idle stage automatically opens the full-screen Song Catalog modal (`#song-catalog-modal`).

## Non-Goals (Out of Scope)
- Syllable-level enhanced LRC word coloring.
- Automatic AI audio-vocal alignment (planned for future major versions).
- Playlists and Favorites management (scoped for Version 0.3.0).

## Functional Requirements

### 1. In-Modal LRC Timestamp Time-Shift Toolbar (`#lyrics-modal`)
- Located directly above `#lyrics-textarea` in the Song Details & Lyrics editor modal.
- **Quick Shift Buttons:**
  - `⏪ -0.5s`
  - `◀ -0.1s`
  - `▶ +0.1s`
  - `⏩ +0.5s`
- **Custom Offset Input:**
  - Number input (step `0.1`s, e.g. `+1.2` or `-0.8`) with an `Apply` button.
- **Behavior:**
  - Reads text from `#lyrics-textarea`, parses every `[MM:SS.xx]` timestamp pattern, adds/subtracts the delta, clamps negative values to `00:00.00`, and replaces the textarea content in real time.
  - Displays an ephemeral badge/alert confirming the shift (e.g. `✓ Shifted timestamps by +0.50s (42 lines updated)`).
  - Works on unsaved or fetched lyrics before clicking `💾 Save Changes`.

### 2. Collapsible Sidebar Accordions in Karaoke Mode
- In Karaoke Mode (`#view-karaoke`), wrap the **Playback Queue** (`#karaoke-card-queue`) and **Song Library** (`#karaoke-card-library`) in accordion header toggles with animated chevrons.
- Persist collapsed/expanded states in `localStorage['flexioke_karaoke_accordions']`.
- Independent state management from Stem Studio accordions.

### 3. Smart Idle Play Action & Empty Queue Fallback
- When stage state is empty (no track active):
  - If `Queue` has $\ge 1$ item: Primary transport play button (`#karaoke-play-pause-btn`) and stage background click trigger `playNext()` from queue.
  - If `Queue` is empty (0 items): Primary transport play button (`#karaoke-play-pause-btn`) and stage background click open `#song-catalog-modal`.

## Acceptance Criteria
- [ ] Clicking any quick time-shift button (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`) in `#lyrics-modal` recalculates all timestamps in `#lyrics-textarea` in-place without dropping non-timestamp text.
- [ ] Timestamps shifted below zero are clamped to `[00:00.00]`.
- [ ] Custom offset input applies positive and negative shifts accurately upon clicking `Apply`.
- [ ] Playback Queue and Song Library in Karaoke Mode can be collapsed and expanded, and states persist across browser reloads.
- [ ] When no song is active and queue has items, clicking Play starts the first queued song.
- [ ] When no song is active and queue is empty, clicking Play opens the Song Catalog modal.
- [ ] 100% automated test coverage for timestamp math, DOM events, and idle play transitions.

## Constraints & Assumptions
- All timestamp shift calculations occur client-side in JavaScript without requiring round-trip API calls.
- Standard LRC format `[MM:SS.xx]` or `[MM:SS.xxx]` is supported.

## Open Questions
- None.
