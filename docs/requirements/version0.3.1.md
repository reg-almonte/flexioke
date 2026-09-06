---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# Requirements: Version 0.3.1 (UI & Stage Experience Enhancements)

## Problem / Motivation
While Flexioke Version 0.3.0 provides robust stem separation, synced lyrics, and playlist management, user feedback identified three key areas for workflow efficiency and presentation quality:
1. **Modal Song Navigation Friction:** When editing metadata, lyrics, or playlist assignments in the `#lyrics-modal`, users must close and reopen the modal for each song. Navigating through a collection of songs is tedious.
2. **Iconography & Visual Hierarchy:** Existing Unicode/emoji button symbols (Play, Restart, Stop, Next, Volume, Settings, Fullscreen, Collapse) lack consistent visual weight and crispness across different operating systems and high-DPI displays, and are hard to replace in a centralized manner.
3. **Non-Immersive Full-Screen Karaoke:** Full-screen mode currently retains static card layouts with visible persistent controls that distract from the singing experience. Live karaoke requires a distraction-free, edge-to-edge cinema display (similar to YouTube/video players) where controls float seamlessly and fade out during active singing.

## Target Users
- **Karaoke Singers & Performers:** Need a clean, immersive, full-screen stage experience with auto-hiding controls and clear lyric highlights.
- **Audio Engineers & Library Curators:** Need rapid navigation between songs in the editor modal to batch-edit titles, artists, and lyrics, and calibrate timing.

## Goals
1. **Seamless In-Modal Song Navigation:** Add Previous (`◀`) and Next (`▶`) controls with track position indicators (`Track X of Y`) inside `#lyrics-modal`, supporting keyboard shortcuts (`Alt + Left/Right`) and unsaved changes confirmation dialogs.
2. **Modern & Modular Icon System:** Replace disparate emojis and Unicode symbols with a centralized, crisp, lightweight SVG icon dictionary for all Karaoke transport, stage controls, modal actions, and Stem Studio channels that can be easily customized in source code.
3. **Immersive YouTube-Style Fullscreen Karaoke Stage:** Provide a true full-screen cinema canvas (`100vw × 100vh`) with floating glassmorphism top header and bottom transport bar that automatically fade out after 3 seconds of inactivity, along with cursor auto-hiding (`cursor: none`) and double-click / `F` key toggle shortcuts.

## Non-Goals (Out of Scope)
- Modifying underlying separation models (Mel-Band RoFormer / UVR Kara 2) or audio DSP pipelines.
- Multi-user authentication or cloud database syncing.
- Hardware video output / multi-monitor secondary display projections (reserved for future versions).

## Functional Requirements

### 1. In-Modal Song Navigation & Unsaved Edits Guard
- **1.1 Modal Header Navigation Controls:**
  - Add Previous (`◀`) and Next (`▶`) navigation buttons in the `#lyrics-modal` header.
  - Display an active position badge (e.g. `Track 3 of 12`) representing the song's current index within the active list context (library search filter, catalog sort, or active playlist).
  - Disable the Previous button on the first track and the Next button on the final track.
- **1.2 Navigation Context Preservation:**
  - When opened from the Stem Studio Library, Karaoke Library, Song Catalog Modal, or Playlist Detail view, the modal inherits that list's filtered and sorted song sequence.
- **1.3 Unsaved Changes Guard:**
  - Track dirty state across title, artist, and lyrics textarea.
  - If the user clicks Previous, Next, or Close while unsaved edits exist, prompt the user: `"You have unsaved changes. Do you want to discard them and proceed?"`.
  - If confirmed, discard edits and navigate/close; if cancelled, stay on the current song.
- **1.4 Keyboard Shortcuts:**
  - Support `Alt + Left Arrow` / `Alt + Right Arrow` (or left/right arrow keys when text fields are not focused) to navigate previous/next songs.

### 2. High-DPI & Modular Iconography Architecture
- **2.1 Centralized SVG Icon Dictionary:**
  - Standardize all action icons into a modular SVG icon system in JavaScript / HTML.
  - Ensure icons scale cleanly on retina / 4K displays and respect CSS theme colors (`currentColor`).
- **2.2 Covered UI Controls:**
  - **Transport Controls:** Play (`▶`), Pause (`⏸`), Restart (`↺`), Next Track (`⏭`), Stop (`⏹`), Master Volume (`🔊` / `🔇`).
  - **Stage Controls:** Settings (`⚙`), Fullscreen Expand (`⛶`), Fullscreen Exit (`✕` / `🗗`), Accordion Toggle (`▾` / `▸`).
  - **Stem Channels:** Instrumental (`🎸`), Lead Vocals (`🎤`), Backing Vocals (`👥`), Export Stems (`📦`).
- **2.3 Enhanced Hotkey Tooltips:**
  - Provide rich tooltips with shortcut cues (e.g., `Play / Pause (Space)`, `Restart (R)`, `Next (N)`, `Fullscreen (F)`).
- **2.4 Developer Extensibility:**
  - Icons defined in a clean, isolated dictionary module (`src/static/icons.js` or dedicated utility) so users/developers can easily substitute alternative SVG glyphs.

### 3. Immersive YouTube-Style Fullscreen Karaoke Stage
- **3.1 True Cinema Canvas (`100vw × 100vh`):**
  - Full-screen mode expands `#karaoke-stage-card` to cover the entire viewport with deep black / dark gradient backdrop and maximized lyrics readability.
- **3.2 Floating Top & Bottom Chrome:**
  - **Top Floating Header:** Translucent pill floating over the stage displaying *Now Singing* (with marquee scroll) and *Up Next* track info, plus an Exit Fullscreen button.
  - **Bottom Floating Transport:** Translucent bottom bar floating above lyrics with Play/Pause, vocal sliders (Lead / Backing / Instrumental), Master Volume, Timecode, and Restart/Next actions.
- **3.3 Inactivity Auto-Hide Engine (3-Second Timeout):**
  - While playing in full-screen, after **3 seconds** of no mouse movement, touch, or keyboard activity, the top header, bottom transport bar, and mouse cursor fade out smoothly (`opacity: 0`, `cursor: none`).
  - Any mouse movement, touch on screen, or keypress immediately restores full visibility (`opacity: 1`, `cursor: default`) and resets the 3-second inactivity timer.
- **3.4 Interactive Stage Shortcuts:**
  - **Double-Click Stage:** Double-clicking anywhere on the lyric stage toggles full-screen mode on/off.
  - **Keyboard Toggle:** Pressing the `F` key toggles full-screen mode on/off.
  - **Stage Click:** Single-clicking the stage while controls are hidden wakes the floating controls.

## Acceptance Criteria
- [ ] Users can click Next / Previous buttons in `#lyrics-modal` to seamlessly cycle through all songs in the current view order.
- [ ] Attempting to navigate away or close `#lyrics-modal` with unsaved changes displays a confirmation dialog preventing accidental data loss.
- [ ] All transport, stage, modal, and channel buttons use crisp, consistent SVG icons with accessible tooltips and shortcut indicators.
- [ ] Fullscreen mode displays edge-to-edge lyrics with floating top and bottom glassmorphism chrome.
- [ ] Floating controls and mouse cursor automatically fade out after 3 seconds of inactivity during fullscreen playback and reappear on user interaction.
- [ ] Double-clicking the stage or pressing `F` reliably toggles fullscreen mode.
- [ ] 100% automated test coverage with zero regressions across existing functionality.

## Constraints & Assumptions
- Pure client-side UI/UX enhancements with zero breaking changes to existing backend REST API schemas.
- Browser Fullscreen API compatibility across standard modern browsers (Chrome, Firefox, Safari, Edge).
- All dynamic HTML generation must pass through `escapeHtml()` to maintain security.

## Open Questions
- None. All behavior validated against user requirements and approved enhancements.
