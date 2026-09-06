---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# Functional Specification: Version 0.3.1 (UI & Stage Experience Enhancements)

## Related Requirements
- `docs/requirements/version0.3.1.md`

---

## 1. Overview
This specification details the technical workflows, DOM component contracts, event listeners, state machines, and styling rules for:
1. **In-Modal Song Navigation & Dirty State Guard** (`#lyrics-modal`).
2. **Centralized Modular SVG Icon Dictionary** (`src/static/icons.js`).
3. **Immersive Full-Screen Cinema Stage & Inactivity Auto-Hide Engine** (`#karaoke-stage-card`).

---

## 2. Functional Flows

### Flow 1: In-Modal Song Navigation (`#lyrics-modal`)
```
[User Clicks "Edit Details / Lyrics" on Song Card]
                      │
                      ▼
[SongLibraryManager.openLyricsModal(jobId, contextList)]
  ├── Stores contextList (array of song objects or job_ids in current view/filter)
  ├── Identifies activeIndex = contextList.findIndex(item => item.job_id === jobId)
  ├── Renders Position Counter: "Track (activeIndex + 1) of contextList.length"
  ├── Sets #modal-nav-prev-btn disabled if activeIndex === 0
  ├── Sets #modal-nav-next-btn disabled if activeIndex === contextList.length - 1
  └── Captures initial clean values: { title, artist, lyrics }
                      │
    ┌─────────────────┴─────────────────┐
    ▼                                   ▼
[User Clicks ◀ Prev / ▶ Next]     [User Presses Alt+Left / Alt+Right]
    │                                   │
    └─────────────────┬─────────────────┘
                      │
                      ▼
          {Has unsaved changes?}
             ├── YES ──► [Show confirm prompt: "You have unsaved changes. Discard and proceed?"]
             │              ├── Cancel ──► [Stay on current song]
             │              └── OK ─────► [Discard changes & proceed]
             └── NO  ──────────────────► [Proceed]
                      │
                      ▼
  [Update activeIndex = activeIndex ± 1]
  [Fetch & Load new song data into modal]
  [Update Position Badge & Button disabled states]
  [Re-render Playlist Checkboxes for new song]
```

### Flow 2: Centralized Modular SVG Icon Dictionary (`src/static/icons.js`)
- **Module Architecture:**
  - Define `window.flexiokeIcons` dictionary object mapping icon names to clean SVG markup with `viewBox="0 0 24 24"` and `currentColor`.
  - Provide utility method `window.getIconHtml(iconName, extraClasses, extraAttrs)`:
    ```javascript
    window.getIconHtml = function(name, extraClasses = '', extraAttrs = '') {
        const svg = window.flexiokeIcons[name];
        if (!svg) return '';
        return `<span class="flexioke-icon flexioke-icon-${name} inline-flex items-center justify-center ${extraClasses}" ${extraAttrs}>${svg}</span>`;
    };
    ```
- **Supported Icon Keys:**
  - `play`, `pause`, `restart`, `next`, `stop`, `volume_high`, `volume_low`, `volume_muted`
  - `settings`, `fullscreen_enter`, `fullscreen_exit`, `chevron_down`, `chevron_right`, `chevron_left`
  - `instrumental`, `lead_vocals`, `backing_vocals`, `zip_export`, `heart_filled`, `heart_outline`
  - `arrow_left`, `arrow_right`, `search`, `close`, `delete`, `edit`, `notes`
- **Extensibility:**
  - To replace or customize an icon, developers modify the SVG template in `src/static/icons.js` without touching component markup.

### Flow 3: Immersive Full-Screen Cinema Stage & Auto-Hide Engine
```
[User Clicks Fullscreen / Presses 'F' / Double-Clicks Stage]
                            │
                            ▼
[KaraokeStageManager.toggleFullscreen()]
  ├── Request browser fullscreen on #karaoke-stage-card (or adds .karaoke-cinema-fullscreen)
  ├── Attaches floating overlay styling to top header and bottom transport
  └── Initializes Inactivity Auto-Hide Watcher
                            │
                            ▼
               {Is Track Currently Playing?}
                  ├── NO  ──► Controls remain persistently visible (opacity: 1)
                  └── YES ──► Start 3000ms inactivity timer
                                 │
                 ┌───────────────┴───────────────┐
                 ▼ (After 3s with no interaction)  ▼ (On mousemove / touch / keypress)
      [Apply .karaoke-chrome-hidden]     [Remove .karaoke-chrome-hidden]
      [Apply .karaoke-cursor-hidden]     [Remove .karaoke-cursor-hidden]
      - Top & bottom bars fade to 0      - Top & bottom bars fade to 1
      - Cursor set to none               - Cursor set to default
      - Stage spans full 100vh           - Restart 3000ms timer
```

---

## 3. UI Components & DOM Specifications

### Component 1: `#lyrics-modal` Header Navigation Toolbar
```html
<div class="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-surface-950">
    <div class="flex items-center gap-3">
        <span class="text-lg">✏️</span>
        <div>
            <h3 class="text-sm font-bold text-white tracking-tight">Edit Song Details & Lyrics</h3>
            <p class="text-[10px] text-slate-400">Manage song metadata, synchronized LRC lyrics, and playlist assignments</p>
        </div>
    </div>
    <div class="flex items-center gap-3">
        <!-- Navigation Sub-Toolbar -->
        <div class="flex items-center gap-1.5 bg-surface-900 border border-slate-800 rounded-xl px-2 py-1">
            <button id="modal-nav-prev-btn" class="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition" title="Previous Song (Alt + Left)">
                <!-- SVG chevron_left -->
            </button>
            <span id="modal-nav-counter-badge" class="text-[11px] font-mono font-semibold text-brand-400 px-1.5 min-w-[70px] text-center select-none">
                Track 1 of 1
            </span>
            <button id="modal-nav-next-btn" class="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition" title="Next Song (Alt + Right)">
                <!-- SVG chevron_right -->
            </button>
        </div>
        <button id="close-lyrics-modal-btn" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition">✕</button>
    </div>
</div>
```

### Component 2: Full-Screen Floating Stage Overlay Layout
- **Container (`#karaoke-stage-card.is-fullscreen`):**
  - Position: `fixed; inset: 0; z-index: 9999; width: 100vw; height: 100vh; background: #030712;`
- **Floating Top Bar (`#karaoke-stage-top-bar`):**
  - Position: `absolute; top: 1.5rem; left: 50%; transform: translateX(-50%); width: calc(100% - 3rem); max-width: 900px; z-index: 30;`
  - Style: Glassmorphism `backdrop-blur-md bg-surface-950/80 border border-slate-800/80 rounded-2xl p-3 shadow-2xl transition-opacity duration-300`
- **Floating Bottom Transport (`#karaoke-stage-transport-bar`):**
  - Position: `absolute; bottom: 1.5rem; left: 50%; transform: translateX(-50%); width: calc(100% - 3rem); max-width: 900px; z-index: 30;`
  - Style: Glassmorphism `backdrop-blur-md bg-surface-950/85 border border-slate-800/80 rounded-2xl p-3.5 shadow-2xl transition-opacity duration-300`
- **Center Stage Lyrics Container (`#karaoke-lyrics-stage`):**
  - Spans full screen height (`height: 100vh; max-height: 100vh; padding-top: 6rem; padding-bottom: 7rem;`) with centered, large-scale lyrics typography.

---

## 4. Business & Interaction Rules

1. **Unsaved Changes State Tracking:**
   - Dirty flag `isDirty` is set to `true` when inputs `#lyrics-edit-title`, `#lyrics-edit-artist`, or `#lyrics-edit-textarea` emit an `input` event differing from their baseline on load.
   - Saving (`#save-lyrics-btn`) or saving lyrics shift clears `isDirty`.
2. **Context Isolation:**
   - When `#lyrics-modal` is triggered from the Song Catalog Modal, navigation operates on the catalog's current sorted/filtered list.
   - When opened from Stem Studio or Karaoke Library, navigation operates on that view's current library list.
   - When opened from a Playlist Detail view, navigation operates within that playlist's track array.
3. **Auto-Hide Inactivity Timer Rules:**
   - Timeout constant: `3000ms`.
   - Timer only counts down when `is_playing === true` AND `is_fullscreen === true`.
   - If playback pauses or stops, controls immediately fade in and timer pauses.
   - Keyboard navigation or transport interaction resets the timer to 3000ms.
4. **Keyboard Accessibility:**
   - `F`: Toggle Fullscreen on/off.
   - `Space`: Play / Pause playback.
   - `R` or `Home`: Restart track from beginning.
   - `N`: Next track in queue.
   - `Esc`: Exit Fullscreen or dismiss open modal.
   - `Alt + Left` / `Alt + Right`: Cycle Previous/Next song in `#lyrics-modal`.

---

## 5. Open Questions
- None. All requirements and behaviors confirmed.
