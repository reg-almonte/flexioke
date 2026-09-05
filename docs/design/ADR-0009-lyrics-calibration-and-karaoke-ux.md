---
status: approved
approved_by: reg
approved_at: 2026-09-05
---

# ADR-0009: Client-Side Synchronized Lyrics Calibration, Karaoke Accordions & Smart Transport Dispatch

## Context & Problem Statement
1. **LRC Timing Calibration:** Synchronized `.lrc` files from external providers or manual transcriptions often exhibit constant time offsets (e.g. ±0.1s to ±2.0s lead or lag). Currently, users must manually rewrite every single timestamp line-by-line.
2. **Karaoke Sidebar Management:** In Karaoke Mode, the Playback Queue and Song Library cards occupy fixed vertical screen real estate and cannot be collapsed to streamline screen space.
3. **Idle Stage Play Action:** Clicking the primary transport Play button or clicking the stage canvas when no song is active is currently a dead end.

## Decision Drivers
- **Zero-Latency Responsiveness:** Timestamp adjustments should happen instantaneously in the browser editor without server round-trips before the user chooses to save.
- **Architectural Simplicity & Reusability:** Accordion mechanics should follow the pattern established in Stem Studio (`localStorage` caching, SVG rotation).
- **Smooth Playback UX:** Clicking Play on an empty stage should immediately start queued music or surface the Song Catalog.

## Considered Options
- **Option 1:** Client-Side Time-Shift Parsing Utility, Native CSS Accordions & Smart Transport Dispatch *(Chosen)*
- **Option 2:** Hybrid Client Editor + Dedicated Server-Side Shift REST Endpoint

## Decision Outcome
**Chosen Option:** **Option 1**.

### Architectural Design:
1. **LRC Time-Shift Parsing Utility (`src/static/library_queue.js`):**
   - Pure function `shiftLrcTimestamps(text, deltaSeconds)`:
     - Matches `\[(\d{2}):(\d{2}(?:\.\d{1,3})?)\]` regex tokens.
     - Calculates new seconds: `clamped = Math.max(0, (minutes * 60 + seconds) + deltaSeconds)`.
     - Formats into zero-padded `[MM:SS.xx]`.
     - Non-timestamp text and metadata tags remain untouched.
   - Wired to quick buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`) and custom offset input in `#lyrics-modal`.
   - Saved via standard `POST /api/jobs/{id}/lyrics` when user clicks `💾 Save Changes`.
2. **Karaoke Sidebar Accordions (`src/static/index.html` & `karaoke_stage.js`):**
   - Headers `#karaoke-queue-header-btn` and `#karaoke-library-header-btn` with toggling on `#karaoke-queue-content` and `#karaoke-library-content`.
   - State stored in `localStorage['flexioke_karaoke_accordions']`.
3. **Smart Idle Transport Dispatch (`src/static/karaoke_stage.js`):**
   - In `handlePlayPause()`: If `!currentJob`, checks `window.flexiokeQueue.queue`.
   - If queue has $\ge 1$ item: calls `window.flexiokeQueue.playNext()`.
   - If queue is empty: calls `window.flexiokeSongLibrary.openCatalogModal()`.

### Positive Consequences
- Sub-millisecond timestamp calculation and visual preview directly in the editor textarea.
- Reuses existing lyrics save endpoint without adding backend route overhead.
- Streamlined, distraction-free Karaoke Mode UI with collapsible cards.
- Seamless one-touch play action from idle stage.

### Negative Consequences / Trade-offs
- Time-shifting math runs in the client browser JavaScript rather than on backend Python service.

## Pros and Cons of the Options

### Option 1: Client-Side Utility, Native Accordions & Transport Dispatch (Chosen)
- **Pros:** Fast, zero backend changes required, minimal network traffic, highly testable in frontend test suite.
- **Cons:** Shifting logic is contained in client JavaScript.

### Option 2: Hybrid Client Editor + Dedicated Server-Side REST Endpoint
- **Pros:** Allows headless/API consumers to shift lyrics on disk without a browser.
- **Cons:** Adds extra server endpoint maintenance, introduces network round-trips for simple text transformations.
