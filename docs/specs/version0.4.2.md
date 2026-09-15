---
status: approved
approved_by: user
approved_at: 2026-09-16
---

# Version 0.4.2: VS Code-Style Resizable Sidebar & Enhanced Karaoke UI — Functional Specification

## Related Requirements
- `docs/requirements/version0.4.2.md`

---

## 1. Overview
This functional specification details the visual components, DOM structures, state machines, event handlers, and responsive layout rules for:
1. **VS Code-Style Activity Bar & Resizable Side Panel** in Karaoke Mode (windowed layout).
2. **Adaptive Stage Header & Prioritized Transport Bar** with responsive width scaling.
3. **Enlarged Fullscreen Cinema Chrome** with 80–90% width transport bar and 24–28px high-DPI icons.
4. **Universal Spacebar Play/Pause Keyboard Shortcut** across Karaoke Mode and Stem Studio.

---

## 2. Functional Flows

### Flow 1: VS Code-Style Activity Bar & Resizable Sidebar (Windowed Layout)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  #karaoke-view (Windowed Mode)                                                         │
├──────────────┬────────────────────────────┬───┬────────────────────────────────────────┤
│ Activity Bar │ Side Panel View            │ S │ Main Karaoke Stage                     │
│ (~48px)      │ (Resizable 0px to 50vw)    │ P │ (flex-1, Responsive Width)             │
│              │                            │ L │                                        │
│ [Queue] (3)  │ ┌────────────────────────┐ │ I │ ┌────────────────────────────────────┐ │
│ [Playlist](5)│ │ Active Tab Content     │ │ T │ │ Dual Stage Header (Now / Up Next)  │ │
│ [Library](42)│ │ (Queue, Playlists, or  │ │ T │ ├────────────────────────────────────┤ │
│              │ │  Song Library)         │ │ E │ │ Lyrics Stage Canvas / HTML5 Video  │ │
│              │ │                        │ │ R │ ├────────────────────────────────────┤ │
│              │ └────────────────────────┘ │   │ │ Responsive Bottom Transport Bar    │ │
│              │                            │   │ └────────────────────────────────────┘ │
└──────────────┴────────────────────────────┴───┴────────────────────────────────────────┘
```

#### Step-by-Step Flow:
1. **Activity Bar Tab Selection:**
   - The user clicks one of the 3 tabs on the left Activity Bar:
     - **Queue Tab (`#tab-karaoke-queue`):** Displays the Playback Queue list with live numeric count badge (`#badge-karaoke-queue`).
     - **Playlists Tab (`#tab-karaoke-playlists`):** Displays Playlists accordion and directory view with playlist count badge (`#badge-karaoke-playlists`).
     - **Song Library Tab (`#tab-karaoke-library`):** Displays the searchable Song Library list with total song count badge (`#badge-karaoke-library`).
   - The clicked tab acquires the active visual state (glowing primary border/accent, high-contrast icon), and `#karaoke-sidebar-content` renders the corresponding view at 100% panel height.
2. **Side Panel Collapse / Expand (Toggle):**
   - If the user clicks the *already active* tab, the side panel collapses: `#karaoke-sidebar-content` transitions to `width: 0px` (or `display: none`), leaving only the 48px Activity Bar visible.
   - Clicking any tab while collapsed expands the side panel to the previously saved width (defaulting to 320px).
   - Pressing `Ctrl+B` or `Cmd+B` (or `Alt+S`) toggles side panel collapse/expand.
3. **Draggable Horizontal Splitter:**
   - The user clicks and drags the vertical splitter handle (`#karaoke-splitter-handle`, ~6px wide).
   - `pointerdown` binds global `pointermove` and `pointerup` listeners with cursor set to `col-resize` and `user-select: none`.
   - As the pointer moves, `#karaoke-sidebar-content` width updates in real-time between minimum (48px / snap-to-collapse) and maximum (50% viewport width).
   - Double-clicking `#karaoke-splitter-handle` instantly resets the side panel to default `320px` width.
4. **State Persistence:**
   - On release or tab toggle, sidebar state is serialized to `localStorage`:
     ```json
     {
       "width": 320,
       "activeTab": "queue",
       "collapsed": false
     }
     ```
   - On application startup, `KaraokeStageManager` reads `localStorage` and restores the exact tab selection, width, and collapsed state.

---

### Flow 2: Responsive Karaoke Stage & Adaptive Transport Bar

```
[Available Stage Width (W)]
    │
    ├──► W >= 640px: Full Layout (Expanded Vocal text "Lead: ON", all transport icons, timecode)
    │
    ├──► 480px <= W < 640px: Compact Layout (Shortened labels "Lead", compact timecode)
    │
    └──► W < 480px: Minimal Layout (Icon-only vocal chips, overflow menu for secondary icons)
```

#### Step-by-Step Flow:
1. **Continuous Responsive Scaling:**
   - As the user resizes the browser window or drags the sidebar splitter, `#karaoke-stage-container` width expands or shrinks dynamically via CSS flexbox.
2. **Dynamic Header Marquee Adjustment:**
   - The dual header banners ("Now Singing" and "Up Next") calculate container bounding width in real-time. If song/artist text exceeds width, CSS marquee scrolling activates automatically.
3. **Prioritized Transport Bar Layout:**
   - **Primary Controls (Always Visible):** Play/Pause button, Restart song button, Volume icon & expandable hover slider, and Lead Vocal toggle button.
   - **Secondary Controls (Responsive Collapse):**
     - When stage width is constrained (< 540px), text labels on Lead and Backing vocal buttons collapse to icon chips (`[Mic: ON]` / `[Chorus: ON]`).
     - When stage width is narrow (< 480px), secondary utility buttons (Stage Settings gear, Timecode display mode toggle, Fullscreen button) collapse into a compact overflow menu (`#karaoke-transport-overflow-btn`) or compact icon bar without wrapping onto multiple vertical lines.

---

### Flow 3: Enhanced Fullscreen Cinema Mode UI

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  #karaoke-stage-card:fullscreen (Cinema Fullscreen Mode)                               │
│                                                                                        │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ [Now Singing: Bohemian Rhapsody - Queen]          [Up Next: Hotel California]  │   │
│   └────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                        │
│                                 (Synchronized Lyrics Display)                          │
│                              "Is this the real life?..."                              │
│                                                                                        │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Floating Transport Bar (Width: 85%, High-DPI Icons: 26px, Large Typography)    │   │
│   │ [Restart] [Play/Pause] [Time: 02:15 / 05:55] [Volume] [Lead Vocal] [Backing]  │   │
│   └────────────────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Step-by-Step Flow:
1. **Fullscreen Transition:**
   - When entering Cinema Fullscreen (`F` key, double-click on stage, or clicking Fullscreen button), the windowed sidebar and activity bar are hidden.
2. **Expanded Floating Glassmorphism Chrome:**
   - The floating transport bar (`#karaoke-cinema-transport`) widens to **85% of screen width** (with a maximum bounding limit of `1200px`).
   - SVG icons scale from standard 18px to **26px** (`w-6.5 h-6.5`).
   - Timecode countdown badge font size increases to `text-base` / `font-bold` for crystal-clear readability from a 10-foot distance.
   - Vocal toggle buttons widen with elevated padding (`px-4 py-2.5`) and distinct glowing active borders.
3. **Stage Header Expansion:**
   - "Now Singing" and "Up Next" banners widen proportionally across the top of the screen with `backdrop-blur-md` and enlarged song title typography (`text-lg md:text-xl`).

---

### Flow 4: Universal Spacebar Play/Pause Keyboard Shortcut

```
[Keydown Event (e.code === 'Space')]
                │
                ▼
  ┌───────────────────────────┐
  │ Active Element Check      │
  │ Is Tag INPUT / TEXTAREA / │
  │ SELECT or ContentEditable?│
  └─────────────┬─────────────┘
                │
        ┌───────┴───────┐
        │               │
     [ Yes ]         [ No ]
        │               │
        ▼               ▼
  [Pass through   [e.preventDefault()]
   to text input] [Toggle active player Play/Pause]
```

#### Step-by-Step Flow:
1. User presses the `Space` key anywhere in the application.
2. Global keydown interceptor inspects `document.activeElement`:
   - If the user is currently typing in search bars (`#studio-search-input`, `#karaoke-search-input`), the lyrics editor (`#lyrics-editor-textarea`), scratchpad notes (`#notes-textarea`), or playlist rename fields, the event passes through untouched so spaces are typed naturally.
3. If focus is outside editable form fields:
   - `event.preventDefault()` is invoked immediately to prevent default browser page scrolling.
   - If in Karaoke Mode, `window.karaokeStage.togglePlay()` is executed.
   - If in Stem Studio, `window.audioPlayer.togglePlay()` is executed.

---

## 3. Inputs & Outputs

| Component / Flow | User Input | Output / State Transition |
|---|---|---|
| **Activity Bar Tab Click** | Click on Tab icon (`Queue`, `Playlists`, `Library`) | Sets active tab, displays full-height view in `#karaoke-sidebar-content`, updates `localStorage`. |
| **Active Tab Re-click** | Click on already active Tab icon | Toggles side panel collapse (`width: 0px`), hides content, updates `localStorage`. |
| **Splitter Drag** | Mouse/pointer drag on `#karaoke-splitter-handle` | Updates `#karaoke-sidebar-content` width dynamically (48px to 50vw). |
| **Splitter Double-Click** | Double-click on `#karaoke-splitter-handle` | Resets side panel width to default 320px. |
| **Keyboard Shortcut `Ctrl+B`** | Press `Ctrl+B` / `Cmd+B` | Toggles side panel collapse/expand. |
| **Stage Resize** | Container width changes (< 640px, < 480px) | Adapts transport bar controls, vocal button labels, and marquee bounding width. |
| **Cinema Fullscreen** | Enter Fullscreen Mode | Expands transport bar to 85% width, scales icons to 26px, enlarges typography. |
| **Spacebar Key** | Press `Space` outside text input | Toggles Play/Pause without browser page scrolling. |

---

## 4. Business & Validation Rules

1. **Activity Bar Invariance:** The left Activity Bar (~48px) is always visible in windowed Karaoke Mode, providing immediate 1-click access to Queue, Playlists, and Library views.
2. **Persistence Integrity:** Sidebar width, active tab index, and collapsed state must survive page reloads and browser tab closures without flash-of-unstyled-content (FOUC).
3. **Text Input Isolation:** The Spacebar shortcut must never interfere with text typing in search fields, lyrics editors, playlist forms, or modal inputs.
4. **Zero Audio / Video Playback Disruption:** Resizing split panels, toggling sidebar tabs, or switching into cinema fullscreen mode must never pause, buffer, or interrupt active WebAudio playback or background video streaming.
5. **Backward Compatibility:** All existing Stage Settings (Geometry controls, transition speeds, countdown thresholds) and dual Side A/B vocal states remain 100% functional.

---

## 5. Data Entities & State Schemas

### Client Storage Entity: `flexioke_karaoke_sidebar_state` (LocalStorage)
```typescript
interface KaraokeSidebarState {
  width: number;        // Side panel width in pixels (default: 320, min: 48, max: 700)
  activeTab: "queue" | "playlists" | "library"; // Current active tab
  collapsed: boolean;   // Whether the side panel content is collapsed
}
```

---

## 6. Open Questions
- None. (All functional flows, responsiveness breakpoints, keyboard bindings, and state persistence rules are fully specified).
