---
status: approved
approved_by: reg
approved_at: 2026-09-05
---

# Functional Specification: Version 0.2.6 (Synchronized Lyrics Calibration & Karaoke UX Enhancements)

## Related Requirements
- `docs/requirements/version0.2.6.md`

---

## 1. Overview
This specification details the user-facing interactions, DOM component behaviors, mathematical parsing algorithms, and client state machines for:
1. **LRC Timestamp Time-Shift Calibration Toolbar** in `#lyrics-modal`.
2. **Collapsible Sidebar Cards** in Karaoke Mode.
3. **Smart Idle Stage Play Action & Empty Queue Fallback**.

---

## 2. Functional Flows

### Flow 1: In-Modal LRC Timestamp Time-Shift Toolbar

```
[User Opens #lyrics-modal] ──► [Lyrics text in #lyrics-textarea]
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
 [Click Quick Button: ±0.1s / ±0.5s]             [Enter Custom Offset + Click Apply]
             │                                                     │
             └──────────────────────────┬──────────────────────────┘
                                        │
                                        ▼
                   [Parse every timestamp [MM:SS.xx]]
                   [New Time = max(0, Old Time + Delta)]
                   [Format back to [MM:SS.xx]]
                                        │
                                        ▼
             [Update #lyrics-textarea in place (No Server Call)]
             [Render Ephemeral Status Badge: "✓ Shifted by ±X.XXs"]
                                        │
                                        ▼
                          [User Clicks "Save Changes"]
                          (Stored permanently via POST /api/jobs/{id}/lyrics)
```

#### Behavioral Rules:
- **Timestamp Regex Pattern:** Supports both standard 2-decimal and 3-decimal patterns: `\[(\d{2}):(\d{2}(?:\.\d{1,3})?)\]`.
- **Mathematical Calculation:**
  $$\text{Total Seconds} = (\text{Minutes} \times 60) + \text{Seconds} + \Delta$$
  $$\text{Clamped Seconds} = \max(0.0, \text{Total Seconds})$$
  $$\text{New Minutes} = \lfloor \text{Clamped Seconds} / 60 \rfloor$$
  $$\text{New Remainder Seconds} = \text{Clamped Seconds} \pmod{60}$$
- **Formatting Output:** Always formats as `[MM:SS.xx]` (two zero-padded digits for minutes, two zero-padded digits with 2 decimal places for seconds).
- **Preservation:** Non-timestamped lines, metadata tags (`[ti:...]`, `[ar:...]`), empty lines, and lyric text remain unaltered.
- **Feedback:** Displays an inline feedback badge for 2.5 seconds: `✓ Shifted timestamps by {+/-}{delta}s ({count} lines updated)`.

---

### Flow 2: Collapsible Sidebar Accordions in Karaoke Mode
- **DOM Structure (`#view-karaoke`):**
  - `#karaoke-card-queue`: Playback Queue accordion container.
    - Header button `#karaoke-queue-header-btn` with title, queue count badge, and `#karaoke-queue-chevron`.
    - Body container `#karaoke-queue-content`.
  - `#karaoke-card-library`: Song Library accordion container.
    - Header button `#karaoke-library-header-btn` with title, song count badge, catalog modal trigger (`⛶`), and `#karaoke-library-chevron`.
    - Body container `#karaoke-library-content`.
- **Interaction:**
  - Clicking the card header toggles the `.hidden` class on the content body with a 180° rotation on the chevron indicator (`rotate-180`).
  - Stored in `localStorage['flexioke_karaoke_accordions']`:
    ```json
    {
      "queue": true,
      "library": true
    }
    ```
  - State loads automatically on page startup and tab switches.

---

### Flow 3: Smart Idle Stage Play Action & Empty Queue Fallback
- **Triggers:**
  1. Primary transport play/pause button (`#karaoke-play-pause-btn` in `#karaoke-transport`).
  2. Clicking the idle stage lyrics background (`#karaoke-stage`).
- **Logic:**
  - If `isPlaying` is `true`: Toggles pause (normal transport behavior).
  - If `isPlaying` is `false` but a track is currently loaded on stage (`currentJob != null`): Resumes playback (normal transport behavior).
  - If no track is currently loaded (`currentJob == null`):
    - **Case A (Queue has $\ge 1$ item):** Calls `window.flexiokeQueue.playNext()` to immediately load and start playing the top queued track.
    - **Case B (Queue is empty):** Opens `#song-catalog-modal` with search focused so the user can pick a song immediately.

---

## 3. UI Wireframes & Component Specs

### `#lyrics-modal` Time-Shift Toolbar Spec
```html
<!-- Timestamp Calibration Toolbar -->
<div class="flex flex-wrap items-center justify-between gap-2 p-2.5 bg-surface-950/80 border border-slate-800/80 rounded-xl text-xs">
    <div class="flex items-center gap-1.5 text-slate-300 font-medium">
        <span>⏱️</span>
        <span>Time-Shift:</span>
    </div>
    <div class="flex items-center gap-1">
        <button type="button" class="lyrics-shift-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 active:bg-slate-900 text-slate-200 text-[11px] font-mono transition" data-shift="-0.5">-0.5s</button>
        <button type="button" class="lyrics-shift-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 active:bg-slate-900 text-slate-200 text-[11px] font-mono transition" data-shift="-0.1">-0.1s</button>
        <button type="button" class="lyrics-shift-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 active:bg-slate-900 text-slate-200 text-[11px] font-mono transition" data-shift="0.1">+0.1s</button>
        <button type="button" class="lyrics-shift-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 active:bg-slate-900 text-slate-200 text-[11px] font-mono transition" data-shift="0.5">+0.5s</button>
    </div>
    <div class="flex items-center gap-1">
        <input type="number" id="lyrics-custom-shift-input" step="0.1" placeholder="±sec" class="w-16 bg-surface-900 border border-slate-700 rounded-lg px-2 py-1 text-[11px] text-slate-200 placeholder-slate-500 font-mono focus:outline-none focus:border-brand-500">
        <button type="button" id="lyrics-custom-shift-btn" class="px-2.5 py-1 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-[11px] font-semibold transition">Apply</button>
    </div>
</div>
```

---

## 4. Acceptance Criteria
- [ ] Clicking any shift button modifies all timestamp lines in `#lyrics-textarea` instantly.
- [ ] Clamping prevents any timestamp from being negative (min `[00:00.00]`).
- [ ] Non-timestamp lines and lyrics text are unchanged.
- [ ] Playback Queue and Song Library in Karaoke Mode can be collapsed and expanded with persistent state in `localStorage`.
- [ ] In Karaoke Mode, clicking Play on an idle stage starts the first queued song if queue is non-empty.
- [ ] In Karaoke Mode, clicking Play on an idle stage with an empty queue opens the Song Catalog modal.
- [ ] All existing test suites pass without regression.
