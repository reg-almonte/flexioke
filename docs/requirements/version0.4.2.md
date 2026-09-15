---
status: approved
approved_by: user
approved_at: 2026-09-16
---

# Version 0.4.2: VS Code-Style Resizable Sidebar & Enhanced Karaoke UI Requirements

## Problem / Motivation
In Version 0.4.1 and prior releases, the Karaoke Mode screen organized the sidebar into vertically stacked accordion cards (Playback Queue, Playlists, Song Library). While functional, this layout suffered from several usability constraints:
1. **Vertical Space Competition:** Having three stacked collapsible accordion cards in a fixed-width sidebar forced users to scroll vertically or constantly collapse/expand accordions when managing the queue, selecting playlists, and searching the library simultaneously.
2. **Fixed Sidebar Geometry:** Users on varying display resolutions (ultrawide monitors, laptops, tablets) could not customize the split ratio between the sidebar management panels and the central lyrics stage.
3. **Transport Bar Responsiveness:** When the screen width was constrained or resized, bottom transport bar controls and vocal toggle buttons did not adapt gracefully, leading to visual crowding.
4. **Fullscreen Cinema Mode Readability:** In Fullscreen Cinema mode, the floating transport chrome remained the same compact size as windowed mode, making transport buttons, timecodes, and icon tooltips difficult to operate and view from a 10-foot distance (living room TV / karaoke party setups).
5. **Keyboard Accessibility:** Global play/pause via the Spacebar was inconsistent or caused browser page scrolling when focus was not explicitly on transport buttons.

## Target Users
- **Karaoke Singers & Party Hosts:** Requiring a high-visibility, immersive stage in fullscreen with easily identifiable controls from across the room.
- **DJs & Session Operators:** Operating in windowed mode who need fast, tabbed switching between the Playback Queue, Playlists, and Song Library, along with a draggable split panel to maximize either stage visibility or song curation workflows.

## Goals
1. **VS Code-Style Activity Bar & Resizable Sidebar:** Implement a modern two-panel layout featuring a slim left Activity Bar (tabs for Playback Queue, Playlists, and Song Library with dynamic count badges) and a draggable vertical splitter divider adjustable from the center down to the tab bar width.
2. **Tabbed Side Panel View with Double-Click & Keyboard Collapse:** Display the selected tab's full-height view on the side panel; clicking the active tab or pressing `Ctrl+B` / `Cmd+B` collapses the panel to activity bar icons only; double-clicking the splitter handle resets to default width (320px).
3. **Responsive Stage Header & Bottom Transport Bar:** Adapt header banners ("Now Singing" / "Up Next") and bottom transport controls to available stage width. Gracefully collapse button text labels, shrink vocal buttons, and prioritize primary controls (Play/Pause, Restart, Volume, Lead/Backing Vocal) over secondary icons on narrow widths.
4. **Enlarged Fullscreen Cinema Chrome:** Widen and expand floating transport bar and stage header to 80–90% stage width in Fullscreen mode, scaling high-DPI icons up to 24px–28px with enlarged typography for 10-foot distance readability.
5. **Universal Spacebar Play/Pause Shortcut:** Provide a robust global Spacebar shortcut across both Karaoke Mode and Stem Studio that toggles playback without scrolling the page (guarded against active text inputs, textareas, and modal form fields).
6. **State Persistence:** Persist sidebar width, active tab index, and collapsed state in `localStorage` across browser reloads.

## Non-Goals (Out of Scope)
- Modifying backend separation algorithms, ML models, or audio processing pipelines.
- Changing API schema contracts or `./data/` storage directory structures.
- Introducing multi-window pop-out displays (deferred to future milestones).

## Functional Requirements

### 1. VS Code-Style Activity Bar & Resizable Side Panel (Windowed Karaoke Mode)
- **1.1 Left Activity Bar:** Fixed slim vertical bar (~48px) containing 3 distinct icon tabs:
  - **Playback Queue Tab:** Queue icon with real-time numeric badge of queued songs.
  - **Playlists Tab:** Playlist icon with badge of available playlists.
  - **Song Library Tab:** Music library icon with badge of total songs.
- **1.2 Active Tab Content Panel:** The side panel displays 100% full-height content of the selected tab (Queue list, Playlists directory/accordion, or Song Library list).
- **1.3 Panel Collapse & Toggle:** Clicking an already active tab collapses the content panel, leaving only the Activity Bar icons visible. Clicking any inactive tab expands the panel to that view.
- **1.4 Draggable Splitter Divider:** A vertical draggable divider between the side panel and main stage allows smooth resizing from center (50% viewport) to minimum tab-bar width (48px).
- **1.5 Splitter Shortcuts & Persistence:**
  - Double-clicking the splitter handle resets the side panel to the default width (320px).
  - Pressing `Ctrl+B` or `Cmd+B` (or `Alt+S`) toggles side panel collapse/expand.
  - Sidebar width, active tab selection, and collapsed state persist in `localStorage` (`flexioke_karaoke_sidebar_state`).

### 2. Responsive Main Stage, Dynamic Header & Adaptive Transport Bar
- **2.1 Responsive Stage Layout:** The central karaoke stage container automatically scales its width to occupy remaining viewport space as the sidebar is resized or collapsed.
- **2.2 Adaptive Stage Header:** Dual header banners ("Now Singing" and "Up Next") dynamically adjust marquee bounding widths and typography size.
- **2.3 Responsive Transport Bar:**
  - Transport bar container width dynamically expands and shrinks with the stage.
  - Lead Vocal and Backing Vocal buttons responsively collapse text labels to compact icons/chips on narrow widths.
  - Controls prioritization: Play/Pause, Restart song, Volume hover slider, and Lead Vocal toggle remain always accessible. Secondary controls (Timecode toggle, Settings gear, Fullscreen toggle) gracefully compact or hide into an overflow menu if width is severely constrained (< 480px stage width).

### 3. Enhanced Fullscreen Cinema Mode UI
- **3.1 Expanded Cinema Transport Bar:** Floating transport bar widens to 80%–90% of fullscreen viewport width with enhanced glassmorphism backdrop.
- **3.2 Scaled-Up High-DPI Iconography & Typography:** Icon sizes increase from 18px to 24px–28px; transport timecode badges and vocal button fonts scale proportionally for effortless visibility from 10+ feet away.
- **3.3 Expanded Stage Header:** Header cards ("Now Singing" / "Up Next") widen and elevate prominence against video and animated lyric backgrounds.

### 4. Universal Spacebar Play/Pause Keyboard Shortcut
- **4.1 Global Play/Pause Binding:** Pressing the `Space` key in either Karaoke Mode or Stem Studio triggers Play/Pause toggle.
- **4.2 Input Focus Guard:** Spacebar shortcut is strictly suppressed when the user is typing inside `<input>`, `<textarea>`, `<select>`, or content-editable elements (such as library search inputs, lyrics editor textarea, notes modal, or playlist rename forms) to prevent accidental playback interruption while typing.
- **4.3 Scroll Suppression:** `event.preventDefault()` is invoked when Spacebar is pressed outside form fields, preventing annoying browser page scroll jumps.

## Acceptance Criteria
- [ ] Left Activity Bar renders 3 tab icons (Queue, Playlists, Library) with live dynamic badge counters.
- [ ] Clicking active tab collapses side panel to activity bar only; clicking inactive tab switches view.
- [ ] Draggable splitter allows smooth horizontal resizing between 48px and 50% viewport width.
- [ ] Double-clicking splitter handle resets side panel to default 320px width.
- [ ] Keyboard shortcut `Ctrl+B` / `Cmd+B` toggles sidebar collapse/expand state.
- [ ] Sidebar width, active tab, and collapsed state persist in `localStorage` across page reloads.
- [ ] Bottom transport bar and vocal buttons responsively adapt on narrow stage widths without layout breaking.
- [ ] Fullscreen Cinema mode floating transport bar expands to 80–90% width with 24–28px enlarged icons.
- [ ] Spacebar universally toggles Play/Pause in Karaoke and Studio modes without scrolling, and is safely ignored during text input.
- [ ] 100% of automated test suites pass without regressions.

## Constraints & Assumptions
- Pure client-side UI and layout enhancement; zero backend schema breaking changes.
- CSS transitions and DOM events must maintain 60fps performance without frame drops during splitter dragging.
- Backward compatibility with existing Stage Settings geometry controls and video backgrounds.

## Open Questions
- None. (All requirements and user preferences resolved during the interview).
