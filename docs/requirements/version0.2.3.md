---
status: approved
approved_by: reg
approved_at: 2026-08-31
---

# Version 0.2.3 — Karaoke Stage UX Refinements, Intro Splash & Song Catalog Modal

## Problem / Motivation
While Version 0.2.2 introduced dual stage headers, marquee scrolling, and queue reordering, live karaoke use revealed several UX friction points:
1. **Abrupt Song Starts:** Songs begin playback instantly without giving the singer time to see the title, artist, and prepare before vocals start.
2. **Countdown Cue Inconsistencies:** Countdown cues occasionally triggered during tight vocal transitions or failed during shorter instrumental interludes (> 5s).
3. **Restart State Drift:** Clicking "Restart Song" reset audio playback to 0:00 but left lyrics scrolled halfway down and previously highlighted lines active until the first line re-triggered.
4. **Limited Stage Highlight Customization:** The active lyric highlight color setting only adjusted border color while keeping a hardcoded cyan background tint.
5. **Sidebar Layout Shift & Crowding:** Variable queue height caused the sidebar to jump between 0, 1, and multiple songs; the song library was excessively tall; and the redundant "Stems ready" badge cluttered cards.
6. **Context-Inappropriate Editing:** The "Edit Details/Lyrics" button in Karaoke Mode was prone to accidental clicks during performance; metadata and lyric editing properly belongs in the Stem Studio workspace.
7. **Restricted Song Browsing:** The narrow 3-card sidebar made exploring larger music collections tedious.

## Target Users
- **Karaoke Singers:** Want a smooth, authentic stage experience with title intro screens, accurate countdown cues, instant song restarts, and clean lyrics styling.
- **Karaoke Hosts / DJ Operators:** Need rapid, full-screen song catalog browsing, stable fixed-height queue layouts, and distraction-free controls without risking accidental lyric edits during a party.

## Goals
- Provide a configurable (0–5s) **Song Intro Splash Card** with delayed audio playback so singers can prepare.
- Ensure **Visual Countdown Cues** reliably trigger 3.0s before singing for long intros (> 5s) and instrumental interludes (> 5s).
- Fix **Restart Song** to instantly scroll the lyrics stage to the top (`scrollTop = 0`) and reset active line highlighting.
- Provide dual color customization in Stage Settings: **Active Glow / Border Color** and **Active Highlight Background / Text Color**.
- Fix the **Playback Queue** height to exactly 3 songs with stable empty states, make the **Song Library** 3 songs tall, and remove `"Stems ready"` badges.
- Restrict the **Edit Details/Lyrics** button exclusively to Stem Studio (hidden in Karaoke Mode and Catalog Modal).
- Introduce a full-screen **Expanded Song Catalog Modal** with fast search, sorting, and 1-click Play Now / Add to Queue.
- Add keyboard shortcuts (`R` / `Home` for Restart, `Esc` for modal dismissals).

## Non-Goals (Out of Scope)
- Cloud/multiplayer synchronized room sharing (deferred to future milestones).
- Video background playback or animated visualizer effects.
- Direct inline editing of lyrics on the live Karaoke Stage.

## Functional Requirements

### 1. Song Title & Artist Intro Splash Screen
- When a song is initiated (via Play Now, Queue auto-advance, or Queue card click), display a prominent **Intro Splash Overlay** on the stage showing `Song Title` and `Artist`.
- **Configurable Duration:** Add an "Intro Splash Duration" slider in Stage Settings (`0s` to `5s`, default `3s`, step `1s`). Setting `0s` bypasses the splash completely.
- **Audio Playback Delay:** When duration $> 0s$, audio playback starts precisely after the splash timer elapses.

### 2. Intelligent Visual Countdown Cue Engine with Configurable Gap Threshold
- Display the 3-beat visual countdown cue (`● ○ ○` → `● ● ○` → `● ● ●`) starting exactly 3.0s before singing under two conditions:
  1. **Song Intro:** First sung lyric timestamp is $\ge$ the configured threshold from the start of playback.
  2. **Instrumental Interlude:** The non-lyric gap between an empty/instrumental line (`♪ ♪ ♪ (Instrumental)`) and the next lyric line is $\ge$ the configured threshold.
- **Configurable Interlude Threshold:** Add a "Countdown Cue Threshold" slider in Stage Settings (`3s` to `5s`, step `1s`, default `3s`).
  - If threshold is `3s`: Gaps $\ge 3.0s$ trigger the 3-second countdown cue starting right as the gap begins.
  - If threshold is `4s` or `5s`: Gaps shorter than the chosen threshold will not trigger the cue; only gaps $\ge 4.0s$ or $\ge 5.0s$ trigger the 3-second countdown (starting at $T - 3.0s$).
- Dismiss the countdown cue smoothly once singing resumes.

### 3. Comprehensive Stage Restart Reset
- When the user clicks the "Restart Song" button (🔄) or presses `R` / `Home`:
  - Seek all audio stems to `0.00s` and resume playback (or trigger intro splash if enabled).
  - Immediately scroll the lyrics stage container to the top (`scrollTop = 0`).
  - Clear and reset all active lyric line highlights and classes.

### 4. Dual Stage Highlight Color Customization
- In Stage Settings (`⚙`), provide two separate color controls:
  1. **Highlight Glow & Border Color:** Customizes the line boundary glow, box shadow, and border tint.
  2. **Highlight Fill & Background Color:** Customizes the background pill highlight and active text styling.
- Real-time CSS variables updated immediately and persisted in `localStorage[flexioke_stage_config]`.

### 5. Fixed-Height Sidebar Layout & Badge Cleanup
- **Fixed Playback Queue Height:** Queue container is set to a fixed height accommodating exactly 3 visible song cards, with a smooth custom scrollbar for overflow and a centered empty state when empty.
- **Shorter Song Library:** Song Library container height adjusted to show 3 visible song cards.
- **Remove "Stems ready" Badges:** Strip the `"Stems ready"` pill from library song cards to maximize space for Title, Artist, and action buttons.

### 6. Mode-Scoped Edit Button Visibility
- The "Edit Details / Lyrics" button (`✏`) is displayed **ONLY** in Stem Studio (Page 1).
- The Edit button is completely removed from Karaoke Mode (Page 2 sidebar and Expanded Catalog Modal) to avoid disruption during singing sessions.

### 7. Expanded Song Catalog Modal
- Add an Expand button (`⛶` / `↗`) at the top right of the Karaoke Song Library header, moving the `N songs` badge to its left.
- Clicking Expand opens a large, responsive **Song Catalog Modal**:
  - Full-width search bar with clear (`✕`) button and title/artist sorting.
  - Rich scrollable list/grid displaying Title, Artist, Duration, and direct action buttons (`▶ Play Now` and `➕ Add to Queue`).
  - Dismissible via `Esc`, close button, or clicking the backdrop overlay.

## Acceptance Criteria
- [ ] Starting a song with Intro Splash set to $N$s displays the splash screen for $N$s and delays audio start by $N$s (0s starts immediately).
- [ ] Countdown cues trigger 3.0s before singing for intros $> 5s$ and interludes $> 5s$.
- [ ] Clicking Restart Song resets audio to 0:00, scrolls lyrics to `scrollTop = 0`, and clears previous active highlights.
- [ ] Stage settings allows picking both highlight glow/border color and highlight background fill color with real-time stage updates.
- [ ] Playback Queue maintains a fixed 3-song height with no layout shift when items are added or removed.
- [ ] Song Library displays 3 cards tall without the `"Stems ready"` text.
- [ ] Edit Details / Lyrics button is visible in Stem Studio and hidden in Karaoke Mode.
- [ ] Clicking the Song Library expand button opens the Catalog Modal with search, sort, and Play/Queue actions.
- [ ] Keyboard shortcut `R` / `Home` restarts the song, and `Esc` closes open modals.

## Constraints & Assumptions
- Fully backwards compatible with existing jobs in `data/jobs/`.
- Zero external client dependencies; pure Tailwind CSS + vanilla ES6+.
- Retains 100% test coverage with automated regression tests.

## Open Questions
- None. All requirements and design choices clarified and agreed upon.
