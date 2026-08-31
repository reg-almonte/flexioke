---
status: approved
approved_by: reg
approved_at: 2026-08-31
---

# ADR-0006: Reactive Stage UX Coordinator, Intro Delay Engine & Client-Side Song Catalog Modal

## Context
Following the release of Version 0.2.2, testing identified several UX friction points during active karaoke use:
1. Songs started playing immediately without visual introductory cues or preparation time for the singer.
2. The visual countdown cue engine lacked a customizable gap threshold, causing inconsistent cue appearances on short or subtle instrumental interludes.
3. The "Restart Song" button re-seeked audio stems to \`0.00s\` but failed to reset the lyrics scroll position to the top or clear active line highlights.
4. The active lyric highlight color setting only adjusted border colors while keeping a hardcoded cyan background tint.
5. Playback Queue height dynamically collapsed or expanded with queue size, creating disruptive sidebar layout shifts.
6. The "Edit Details / Lyrics" button was visible in Karaoke Mode, creating a risk of accidental edits during performances.
7. The narrow 3-card sidebar limited rapid song browsing in large music libraries.

## Decision
We chose **Option 1: Unified Client-Side State Machine & Reactive Song Catalog**:
1. **Intro Splash Timer & Audio Pre-buffering:** Implement \`introSplashTimer\` in \`KaraokeStageManager\`. When a song loads, audio stems buffer in the background while an animated Title & Artist overlay is presented for the user-configured duration ($0–5$s, default $3$s). Audio playback starts automatically the instant the timer finishes ($0$s starts immediately).
2. **Configurable Countdown Cue Evaluator:** Enhance the countdown evaluator with a configurable threshold ($3–5$s, default $3$s) stored in \`localStorage["flexioke_stage_config"]\`. Cues reliably trigger $3.0$s before singing resumes when gap $\ge$ threshold.
3. **Atomic Stage Restart Coordinator:** Update the Restart action to atomically seek stems to \`0.00s\`, scroll the lyrics stage container immediately to the top (\`scrollTop = 0\`), and reset active highlight indexes and CSS classes.
4. **Dual CSS Custom Properties for Lyric Highlighting:** Expose two distinct CSS custom properties (\`--karaoke-highlight-color\` for glow/borders and \`--karaoke-highlight-fill\` for background pill tint) with dedicated color pickers in the Stage Settings modal.
5. **Fixed Sidebar Viewports & Clean Cards:** Set the Playback Queue container to a fixed 3-card height (\`h-[196px]\`) with centered empty state, adjust Song Library to 3 cards tall (\`h-[210px]\`), and remove `"Stems ready"` badges from song cards.
6. **Context-Scoped Permissions:** Render the \`Edit Details / Lyrics\` button (\`.edit-lyrics-btn\`) exclusively in Stem Studio (Page 1), stripping it from Karaoke Mode (Page 2 sidebar and Catalog Modal).
7. **Expanded Song Catalog Modal:** Implement \`#song-catalog-modal\` driven by \`SongLibraryManager\` using the cached in-memory library collection for instant client-side filtering, sorting (A-Z, Z-A, Recent), and direct \`Play Now\` and \`Add to Queue\` actions.
8. **Keyboard Bindings:** Bind \`R\` / \`Home\` to Restart Song and \`Esc\` to dismiss all open modals.

## Options Considered

### Option 1: Unified Client-Side State Machine & Reactive Song Catalog (Chosen)
- **Pros:**
  - Zero server network latency; instant search filtering and modal interactions.
  - Seamless background audio stem pre-buffering during intro splash.
  - Clean separation of UI permissions between Studio and Karaoke views.
  - Fixed-height grid containers eliminate layout shifting.
- **Cons:**
  - Catalog filtering is executed client-side (optimal for collections up to thousands of songs).

### Option 2: Server-Side Paginated Catalog & Backend Playback Scheduler
- **Pros:**
  - Supports massive enterprise multi-tenant catalogs exceeding 100,000 tracks.
- **Cons:**
  - Unnecessary complexity, API overhead, and network latency for a standalone local desktop karaoke application.
  - Potential audio lag following intro splash completion due to network roundtrips.

## Consequences
- **Positive:**
  - Drastically improved stage presentation and performer preparation via intro splash and accurate countdowns.
  - Elimination of all layout jumps and accidental lyric editing in Karaoke Mode.
  - Fast, intuitive song discovery with full-screen catalog browsing and sorting.
- **Negative / Neutral:**
  - Requires updating stage test suites to account for intro delay buffering, dual highlight color variables, and fixed-height DOM containers.

## Related
- **Functional spec:** `docs/specs/version0.2.3.md`
- **Requirement:** `docs/requirements/version0.2.3.md`
- **Supersedes / related ADRs:** Extends `docs/design/ADR-0005-karaoke-stage-transport-queue-reordering.md` and `docs/design/ADR-0004-karaoke-metadata-and-stage-enhancements.md`.
