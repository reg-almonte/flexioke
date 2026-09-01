---
status: approved
approved_by: reg
approved_at: 2026-09-01
---

# ADR-0008: In-Process LRCLIB Client with Dual Pipeline Auto-Sync & Interactive Proxy

## Context & Problem Statement
Karaoke and Stem Studio users currently need to manually discover, format, and paste synchronized `.lrc` lyrics into Flexioke. LRCLIB (`https://lrclib.net/`) offers a free, open-access, zero-authentication public REST API containing timestamped synchronized lyrics. We need an architectural approach that enables both automated lyric synchronization during background stem separation and 1-click on-demand lyric search/retrieval in the frontend Song Details & Lyrics editor modal.

## Decision Drivers
- **Zero Configuration / Keyless Access:** Seamless integration without requiring API keys or user sign-ups.
- **Dual Availability (Auto + Fallback):** Automatic background syncing on ingestion plus 1-click manual retry in the UI.
- **Resilience & Fault Tolerance:** Failure to retrieve lyrics from LRCLIB must never fail stem separation.
- **CORS Immunity & Standard Compliance:** Compliant `User-Agent` telemetry without browser CORS restrictions.
- **Minimal Dependencies:** Use standard library networking (`urllib`, `certifi`, `json`, `ssl`).

## Considered Options
1. **Option 1: In-Process Python LRCLIB Client with Dual Pipeline Auto-Sync & Interactive REST Proxy (Chosen)**
2. **Option 2: Direct Frontend Browser-Side Fetching Only**

## Decision Outcome
Chosen **Option 1**: Implement an in-process LRCLIB client module (`src/services/lrclib_client.py`) on the FastAPI backend, integrated into both the `pipeline.py` separation workflow and exposed through proxy REST endpoints (`GET /api/lyrics/lrclib/get` and `/search`) for the `#lyrics-modal` UI.

### System Architecture
```
┌───────────────────────────────────────────────┐
│                 Flexioke Core                 │
│                                               │
│  [Audio Ingestion / URL Download]             │
│        │                                      │
│        ▼                                      │
│  [Smart Title/Artist Parser]                  │
│        │                                      │
│        ├────────────────────────────────┐     │
│        ▼                                ▼     │
│  [Separation Pipeline]        [lrclib_client.py] ────► [LRCLIB REST API]
│  (RoFormer + UVR Karaoke)               │     │        (https://lrclib.net)
│        │                                │     │
│        ▼                                ▼     │
│  [Final MP3 Stems] ◄────── [Auto-Saved lyrics.lrc]
│                                               │
│  [Song Details Modal (UI)]                    │
│        │                                      │
│        ▼                                      │
│  [GET /api/lyrics/lrclib/get] ────────────────┘
└───────────────────────────────────────────────┘
```

### Positive Consequences
- **Automated Workflow:** Uploaded or downloaded songs automatically gain synchronized karaoke lyrics with zero clicks.
- **Interactive Control:** If the initial auto-match misses, users can adjust Title/Artist and click `⚡ Auto-Fetch LRC` inside `#lyrics-modal` for instant 1-click population.
- **No CORS Issues:** All external requests originate from the backend with standard `User-Agent: Flexioke/0.2.5 (https://github.com/reg-almonte/flexioke)` headers.
- **Zero Additional Packages:** Built using Python's standard `urllib` and `ssl` modules with `certifi`.

### Negative Consequences / Trade-offs
- Outbound network requests add ~100–300ms during ingestion (handled asynchronously in worker thread).
- Dependent on LRCLIB uptime (mitigated by non-blocking `try...except` fallback logic).

## Pros and Cons of the Options

### Option 1: In-Process Python LRCLIB Client with Dual Auto-Sync & REST Proxy
- **Good:** Works seamlessly for headless batch uploads, URL downloads, and interactive UI.
- **Good:** Complete immunity from browser-side CORS and ad-blockers.
- **Good:** Automatic fallback from exact match (`/api/get`) to fuzzy search (`/api/search`).
- **Bad:** Backend requires outbound HTTPS internet access.

### Option 2: Direct Frontend Browser-Side Fetching Only
- **Good:** Keeps the backend codebase purely local with no external HTTP clients.
- **Bad:** Cannot auto-populate lyrics during batch background separation or when the browser tab is closed.
- **Bad:** Prone to client-side CORS or browser privacy extension blocking.

## Implementation Plan
1. **`src/services/lrclib_client.py`:** Create LRCLIB client class with `get_lyrics(title, artist, duration)` and `search_lyrics(query)`.
2. **`src/api/routes.py`:** Add `GET /api/lyrics/lrclib/get` and `GET /api/lyrics/lrclib/search` endpoints.
3. **`src/services/pipeline.py`:** Add automated background lyrics check & save step upon audio ingestion.
4. **`src/static/index.html` & `src/static/library_queue.js`:** Add `⚡ Auto-Fetch LRC` button and async handler inside `#lyrics-modal`.
5. **`tests/`:** Add unit and integration tests covering LRCLIB parsing, API routes, pipeline auto-sync, and error scenarios.
