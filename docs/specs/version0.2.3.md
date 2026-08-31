---
status: approved
approved_by: reg
approved_at: 2026-08-31
---

# Version 0.2.3 — Karaoke Stage UX Refinements, Intro Splash & Song Catalog Modal — Functional Spec

## Related Requirements
- `docs/requirements/version0.2.3.md`

## Functional Flows

### 1. Song Title & Artist Intro Splash Flow
#### Main Flow
1. User starts a song via **Play Now** on a library card, **Play Now** in the Catalog Modal, or automatic queue advancement.
2. The system checks \`config.introSplashDuration\` (integer $0–5$s, default $3$s).
3. If \`introSplashDuration > 0\`:
   - An animated **Intro Splash Card** overlays the lyrics stage displaying:
     - Song Title in bold primary typography (\`text-2xl font-black\`).
     - Artist name in subtitle typography (\`text-sm font-semibold text-brand-300\`).
     - A subtle countdown/progress pulse indicating time until music starts.
   - Stage lyrics container is hidden or blurred behind the splash card.
   - Audio playback start is delayed by exactly \`introSplashDuration\` seconds.
4. After \`introSplashDuration\` seconds:
   - The splash card smoothly fades out.
   - Stage lyrics become active and visible.
   - Multitrack audio playback starts immediately locked to timestamp \`0.00s\`.

#### Alternate / Bypass Flows
- If \`introSplashDuration == 0\`: The intro splash is completely bypassed; audio starts immediately at \`0.00s\` with lyrics displayed right away.
- If user clicks **Restart Song** (🔄): If \`introSplashDuration > 0\`, the splash screen re-displays for \`introSplashDuration\` before resuming at \`0.00s\`. If user clicks **Play/Pause** to unpause mid-song, the splash does *not* re-trigger.

---

### 2. Configurable Visual Countdown Cue Flow
#### Main Flow
1. As the audio playback position advances, the countdown cue evaluator checks:
   - Current track time \`T_curr\`
   - Next lyric line start time \`T_next\`
   - Previous lyric line end time (or track start \`0.00s\`) \`T_prev\`
   - Configured threshold \`config.countdownThreshold\` ($3$s to $5$s, default $3$s).
2. If \`(T_next - T_prev) >= config.countdownThreshold\`:
   - Countdown triggers when \`T_curr >= (T_next - 3.0s)\` and \`T_curr < T_next\`.
   - Beat 1 (\`● ○ ○\`): Displayed from \`T_next - 3.0s\` to \`T_next - 2.0s\`.
   - Beat 2 (\`● ● ○\`): Displayed from \`T_next - 2.0s\` to \`T_next - 1.0s\`.
   - Beat 3 (\`● ● ●\`): Displayed from \`T_next - 1.0s\` to \`T_next\`.
3. At \`T_curr >= T_next\`, the countdown cue element is immediately hidden (\`.classList.add("hidden")\`) and the active line highlights.

#### Alternate Flows
- If the gap between lines is $< \text{config.countdownThreshold}$ (e.g. gap is 2.5s when threshold is 3s, or gap is 3.5s when threshold is 4s), the countdown cue does NOT trigger.

---

### 3. Stage Restart & Lyric State Reset Flow
#### Main Flow
1. User clicks the **Restart Song** button (🔄) on the bottom transport bar, or presses \`R\` / \`Home\` on the keyboard.
2. The player halts all in-flight audio, locks seek synchronization (\`isSyncingSeek = true\`), aligns all stem playheads simultaneously to \`0.00s\`.
3. The stage manager:
   - Scrolls the lyrics container immediately to the top (\`scrollTop = 0\`).
   - Clears \`activeLineIndex = -1\` and resets styling on previously highlighted elements.
   - Clears and hides any active countdown cue elements.
4. If \`introSplashDuration > 0\`, triggers the intro splash countdown before audio playback begins; otherwise resumes playback immediately.

---

### 4. Dual Stage Highlight Color Configuration Flow
#### Main Flow
1. User opens Stage Settings (\`⚙\`).
2. Two color pickers are available:
   - **Highlight Glow / Border Color** (\`#settings-highlight-glow-color\`): Controls CSS variable \`--karaoke-highlight-color\`, border color, and outer glow box-shadow.
   - **Highlight Fill / Background Color** (\`#settings-highlight-fill-color\`): Controls CSS variable \`--karaoke-highlight-fill\`, background pill tint, and active text glow.
3. Modifying either input instantly updates the CSS root variables and all rendered stage lines in real-time.
4. Settings are persisted automatically into \`localStorage["flexioke_stage_config"]\`.

---

### 5. Fixed-Height Sidebar & Badge Cleanup Flow
#### Main Flow
1. **Playback Queue Container:** Fixed height set to \`h-[196px]\` (or fixed 3-card height) with \`overflow-y-auto\`.
   - When 0 songs are queued, displays a centered, non-collapsing empty state.
   - When 1–3 songs are queued, displays cards with full height stability.
   - When $> 3$ songs are queued, displays 3 cards with smooth scrolling for additional items.
2. **Song Library Container:** Compact height set to \`h-[210px]\` (or 3 visible cards) with \`overflow-y-auto\`.
3. **Card Presentation:** Library cards remove the \`Stems ready\` badge and display:
   - Row 1: Song Title (bold, truncated).
   - Row 2: Artist Name (\`text-slate-400\`).
   - Actions: \`▶ Play\` and \`➕ Queue\` (in Karaoke view).

---

### 6. Mode-Scoped Edit Button Visibility Flow
#### Main Flow
1. When rendering Song Library cards:
   - In **Stem Studio** (Page 1): Render \`▶ Play\`, \`➕ Queue\`, and \`✏ Edit Details/Lyrics\` (\`.edit-lyrics-btn\`).
   - In **Karaoke Mode** (Page 2 Sidebar & Catalog Modal): Omit \`.edit-lyrics-btn\` completely. Only \`▶ Play\` and \`➕ Queue\` are rendered.

---

### 7. Expanded Song Catalog Modal Flow
#### Main Flow
1. User clicks the **Expand** button (\`⛶\` / \`↗\`) at the top right of the Karaoke Song Library card.
2. The system opens \`#song-catalog-modal\`:
   - Displays full catalog count in header: \`📚 Song Catalog (N Songs)\`.
   - Search bar with automatic autofocus, real-time debounced filtering, and \`✕\` clear button.
   - Sort dropdown: \`Title (A-Z)\`, \`Title (Z-A)\`, \`Artist (A-Z)\`, \`Recently Added\`.
   - Scrollable catalog table / grid displaying Song Title, Artist, Duration, and action buttons:
     - \`▶ Play Now\`: Starts song immediately (with interruption check if a track is playing).
     - \`➕ Add to Queue\`: Adds to playback queue with animated toast / visual confirmation badge.
3. Modal can be dismissed via:
   - Close button (\`✕\`).
   - Clicking outside the modal on the backdrop overlay.
   - Pressing the \`Esc\` key.

---

## Inputs & Outputs

### 1. Stage Configuration Schema (\`localStorage["flexioke_stage_config"]\`)
| Field | Type | Default | Valid Range | Description |
|---|---|---|---|---|
| \`introSplashDuration\` | integer | \`3\` | \`0\` – \`5\` | Seconds to display title splash and delay playback start (0 = off). |
| \`countdownThreshold\` | integer | \`3\` | \`3\` – \`5\` | Minimum gap duration (seconds) required to trigger countdown cues. |
| \`baseFontSizePx\` | integer | \`20\` | \`14\` – \`28\` | Base font size in px for inactive lyrics lines. |
| \`activeFontSizePx\` | integer | \`24\` | \`16\` – \`28\` | Font size in px for the active singing line. |
| \`activeHighlightGlowColor\` | string | \`"#06b6d4"\` | Valid hex color | Border and glow box-shadow accent. |
| \`activeHighlightFillColor\` | string | \`"#0891b2"\` | Valid hex color | Pill background fill tint & highlight accent. |

### 2. DOM Events & Keybindings
| Trigger / Key | Context | Action |
|---|---|---|
| \`R\` or \`Home\` | Karaoke Mode | Triggers \`KaraokeStageManager.restartSong()\` |
| \`Esc\` | Any Modal Open | Closes Settings Modal, Catalog Modal, or Confirmation Modal |
| Expand Button | Song Library Card | Opens \`#song-catalog-modal\` and focuses search input |

---

## Business Rules & Invariants
1. **Zero Layout Shifts:** Fixed container heights on sidebar cards ensure the Karaoke Stage card position never shifts when queue state changes.
2. **Audio Delay Integrity:** When \`introSplashDuration > 0\`, stem decoders buffer and prepare during the splash phase so audio starts instantly and cleanly with zero lag once the timer fires.
3. **Performance Safety:** In Karaoke Mode, singers and audience members cannot accidentally open the lyric editor or mutate stored song metadata.
4. **Backward Compatibility:** All existing jobs and settings configs without the new fields fallback cleanly to their default values (\`introSplashDuration = 3\`, \`countdownThreshold = 3\`, \`activeHighlightFillColor = "#0891b2"\`).

## Open Questions
- None. All functional flows and edge cases defined.
