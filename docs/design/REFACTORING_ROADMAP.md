# Flexioke Architectural Refactoring Roadmap & Technical Debt Remediation Plan
**Status:** Active  
**Version:** 0.4.1  
**Date:** 2026-09-14  
**Author:** AI-DLC Architecture & Engineering Team (EPIC-0012 / STORY-0039 / TASK-0080)  
**Baseline Artifact:** `tests/ASSESSMENT_REPORT.md`

---

## 1. Executive Context & Objectives

During the Version 0.4.1 7-dimensional code quality, security, and performance audit (`tests/ASSESSMENT_REPORT.md`), the Flexioke codebase earned an overall **Quality Score of 8.9/10 (Grade: A-)** with 194/194 automated test suites running cleanly in ~6 seconds.

While core processing, concurrency locks, WebAudio routing, and file durability are exceptionally robust, rapid feature additions across versions 0.1.0 through 0.4.0 created architectural technical debt in two primary areas:
1. **Monolithic API Router:** `src/api/routes.py` (835 lines) concentrates 30+ endpoints across 7 domains into a single file.
2. **Frontend Controller Sizing & Imperative State Coupling:** `src/static/karaoke.js` (1,538 lines) and `src/static/library_queue.js` (1,430 lines) contain multiple distinct modal and UI controllers, communicating via direct imperative invocations on global `window.*` objects.

This roadmap defines an actionable, phased refactoring plan to modularize these components while guaranteeing **100% backward compatibility, zero breaking API changes, and 100% test pass rate throughout all transitions**.

---

## 2. Refactoring Architecture Strategy

```
CURRENT ARCHITECTURE (v0.4.1)                  REFACTORED MODULAR ARCHITECTURE (v0.4.2+)
┌──────────────────────────────────────┐       ┌────────────────────────────────────────────────────────┐
│  src/api/routes.py (835 lines)       │       │  src/api/                                              │
│  - /jobs (upload, side-ab, url, etc.)│       │  ├── jobs.py       (Upload, Side-AB, Download, Status) │
│  - /queue                            │  ───► │  ├── queue.py      (Add, Next, Reorder, Play-Now)      │
│  - /playlists                        │       │  ├── playlists.py  (CRUD, Favorites, Reorder)          │
│  - /lyrics & lrclib                  │       │  ├── lyrics.py     (Editor persistence, LRCLIB proxy)  │
│  - /videos                           │       │  ├── videos.py     (Auto-discovery, HTTP 206 range)    │
│  - /health                           │       │  └── health.py     (Status check)                      │
└──────────────────────────────────────┘       └────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐       ┌────────────────────────────────────────────────────────┐
│  src/static/library_queue.js (1430L) │       │  src/static/                                           │
│  - Library rendering & search        │       │  ├── library.js        (Core list & instant search)    │
│  - Ingestion (upload, URL, side-ab)  │  ───► │  ├── uploader.js       (Drag-drop batch & Side A/B)    │
│  - Song Details & Lyrics editor modal│       │  ├── lyrics_modal.js   (Editor, LRCLIB sync, calib)    │
│  - Expanded Catalog modal            │       │  ├── catalog_modal.js  (Modal catalog & batch actions) │
│  - Queue list rendering              │       │  └── event_bus.js      (Typed pub/sub event contracts) │
└──────────────────────────────────────┘       └────────────────────────────────────────────────────────┘
```

---

## 3. Technical Debt Remediation Backlog

### Phase 1: Modularization & Decoupling (Version 0.4.2 Target)

#### REF-01: Decompose `src/api/routes.py` into Modular `APIRouter` Submodules
- **Category:** Backend Maintainability & Modularity
- **Scope:** 
  - Create package `src/api/` with individual route modules:
    - `src/api/jobs.py` (Ingestion, status polling, cancellation, zip export)
    - `src/api/queue.py` (Queue mutations, reordering, playback dispatch)
    - `src/api/playlists.py` (Playlist CRUD, favorite toggles, song assignment)
    - `src/api/lyrics.py` (Lyrics CRUD, timestamp shifting, LRCLIB search/fetch)
    - `src/api/videos.py` (Video auto-discovery, HTTP 206 range streaming)
    - `src/api/health.py` (Service health endpoint)
  - Combine submodules in `src/api/__init__.py` using `APIRouter.include_router()`.
- **Impact:** Eliminates monolithic file, simplifies PR reviews, maps 1-to-1 with `tests/api/` test suites.
- **Risk / Mitigation:** Low risk. FastAPI routing precedence is preserved by maintaining identical URL path prefixes.

#### REF-02: Decompose `src/static/library_queue.js` into Focused UI Modules
- **Category:** Frontend Maintainability & Single Responsibility
- **Scope:**
  - Extract `src/static/lyrics_modal.js`: Manages Song Details modal, LRCLIB auto-fetch, and timestamp shift calibration toolbar.
  - Extract `src/static/catalog_modal.js`: Manages Expanded Song Catalog modal, search filters, and 1-click queue/play actions.
  - Extract `src/static/uploader.js`: Manages drag-and-drop batch upload area, direct audio URL downloader, and Side A/B upload modal.
  - Retain core `library.js` for primary sidebar library rendering and queue list.
- **Impact:** Reduces file complexity from 1,430 lines to four cohesive files of ~250–400 lines each.
- **Risk / Mitigation:** Low risk. Use standardized DOM ID selectors and script tag ordering in `src/static/index.html`.

#### REF-03: Introduce Lightweight Frontend Event Bus (`event_bus.js`)
- **Category:** Frontend Architecture & Decoupling
- **Scope:**
  - Implement a zero-dependency event bus using standard browser `EventTarget` in `src/static/event_bus.js`.
  - Define explicit typed event channels:
    - `flexioke:track:loaded` (payload: `{ jobId, trackData }`)
    - `flexioke:track:playing` / `flexioke:track:paused` / `flexioke:track:ended`
    - `flexioke:queue:updated` (payload: `{ queue, currentTrack }`)
    - `flexioke:playlist:updated` (payload: `{ playlistId }`)
    - `flexioke:lyrics:updated` (payload: `{ jobId, lyrics }`)
    - `flexioke:favorites:toggled` (payload: `{ songId, isFavorite }`)
  - Migrate imperative cross-calls (`window.karaokeStage.update()` or `window.audioPlayer.play()`) to reactive event listeners.
- **Impact:** Eliminates circular dependencies and temporal initialization races between player, karaoke stage, and library controllers.

#### REF-04: Parameter Nomenclature Standardization (`song_id` vs `job_id`)
- **Category:** API Consistency & Domain Alignment
- **Scope:**
  - Standardize API request/response models and internal dictionary keys to treat `song_id` as an alias for `job_id`.
  - Provide bidirectional compatibility in Pydantic models with `Field(validation_alias=...)` so both legacy `job_id` and modern `song_id` are accepted transparently.
- **Impact:** Improves semantic clarity when dealing with non-separation tracks (e.g. Side A/B uploads).

---

### Phase 2: Performance, Streaming & State Unification (Version 0.5.0 Target)

#### REF-05: Real-Time Pipeline Progress via Server-Sent Events (SSE)
- **Category:** Efficiency, Scalability & UX
- **Scope:**
  - Add SSE streaming endpoint `GET /api/jobs/{job_id}/progress/sse` in FastAPI using `asyncio` or `starlette.responses.EventSourceResponse`.
  - Frontend connects via `new EventSource()` on job submission, replacing client-side 1-second `setInterval` polling loops.
- **Impact:** Drastically reduces HTTP request volume during long 2-stage separation jobs, yielding instant progress bar updates.

#### REF-06: Unified Client State Store (`state_store.js`)
- **Category:** Reliability & Client Architecture
- **Scope:**
  - Implement a centralized single-source-of-truth state container for active mode (Studio vs Karaoke), volume levels, vocal mute states, fullscreen status, and loaded track metadata.
  - Automatically synchronize persistent preferences (theme, geometry, accordion states) with `localStorage`.
- **Impact:** Prevents UI state desynchronization across modals and multi-screen karaoke sessions.

---

## 4. Step-by-Step Implementation & Verification Protocol

To ensure seamless execution without introducing regressions, all refactoring steps must adhere to the following 5-point protocol:

1. **Test-First Seam Verification:**
   Before extracting code, run the domain test suite (`pytest tests/api/`, `pytest tests/frontend/`) to confirm baseline green state.
2. **Incremental Extraction:**
   Extract one submodule at a time (e.g. extract `src/api/jobs.py` first, run `pytest`, then extract `src/api/playlists.py`).
3. **Dual Headless & Browser Validation:**
   Run `pytest` (including Node.js DOM simulations) and perform human browser smoke tests across Stem Studio, Karaoke Stage, and Modals.
4. **Zero Breaking Schema Changes:**
   Ensure all existing REST endpoints, JSON field names, and HTTP status codes remain identical.
5. **Phase 4.5 PR Review Audit:**
   Each refactoring task branch is submitted to automated subagent PR review before merging into `master`.

---

## 5. Summary Roadmap Milestones

| Milestone | Target Version | Key Deliverables | Expected Completion |
|---|---|---|---|
| **Phase 1** | **Version 0.4.2** | REF-01 (API Router decomposition), REF-02 (Frontend module split), REF-03 (Event Bus), REF-04 (Parameter aliasing) | Next Cycle |
| **Phase 2** | **Version 0.5.0** | REF-05 (Server-Sent Events for job progress), REF-06 (Unified Client State Store) | Future Cycle |

---

## 6. Conclusion

This Refactoring Roadmap provides a concrete, low-risk engineering path to evolve Flexioke from its current monolithic structure into a highly modular, decoupled, and maintainable architecture while preserving its core strengths of speed, zero external dependencies, and local reliability.
