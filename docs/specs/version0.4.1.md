---
status: pending-approval
approved_by:
approved_at:
---

# Functional Specification: Version 0.4.1 (Code Quality, Performance Assessment & Test Suite Reorganization)

## Related Requirements
- `docs/requirements/version0.4.1.md`

---

## 1. Overview
This functional specification details the operational structure, evaluation framework, artifact layout, and validation rules for:
1. **Modular Test Suite Reorganization** (migrating flat `tests/` files into categorized subdirectories `api/`, `services/`, `frontend/`, `integration/` with zero broken dependencies).
2. **Comprehensive 7-Dimensional Code Quality, Security & Performance Assessment** (evaluating backend architecture and frontend modules, outputting `tests/ASSESSMENT_REPORT.md`).
3. **Refactoring & Architecture Evolution Roadmap** (authoring the redesign plan in `docs/design/`).

---

## 2. Functional Flows

### Flow 1: Modular Test Suite Reorganization
```
[tests/ (40+ flat test files)]
             │
             ├──► tests/api/          (Route endpoints, HTTP status codes, request/response models)
             ├──► tests/services/     (Pipeline, workers, managers, persistence, audio validators)
             ├──► tests/frontend/     (DOM rendering, WebAudio gain matrices, Node.js simulations)
             └──► tests/integration/  (Milestone end-to-end flows, cross-service regressions)
             │
             ▼
[pytest execution from repo root] ──► 194/194 tests discovered and passing cleanly
```

#### Detailed Folder Mapping:
1. **`tests/api/` (12 files):**
   - `test_audio_url_api.py`, `test_frontend_routes.py`, `test_health.py`, `test_job_cancellation.py`, `test_library_api.py`, `test_lrclib_api.py`, `test_lyrics_api.py`, `test_playlist_api.py`, `test_side_ab_api.py`, `test_upload_api.py`, `test_video_api.py`, `test_youtube_api.py`.
2. **`tests/services/` (12 files):**
   - `test_audio_downloader.py`, `test_audio_validator.py`, `test_job_manager.py`, `test_lrclib_client.py`, `test_lyrics_store.py`, `test_pipeline_and_stems.py`, `test_playlist_manager.py`, `test_queue_service.py`, `test_stage1_separator.py`, `test_stage2_separator.py`, `test_track_export_and_cleanup.py`, `test_video_manager.py`.
3. **`tests/frontend/` (16 files):**
   - `test_favorites_frontend.py`, `test_karaoke_cinema_fullscreen.py`, `test_karaoke_controls_and_interruption.py`, `test_karaoke_fullscreen.py`, `test_karaoke_navigation.py`, `test_karaoke_playlists_frontend.py`, `test_karaoke_stage.py`, `test_karaoke_video_stage.py`, `test_library_queue_frontend.py`, `test_lyrics_modal_frontend.py`, `test_lyrics_modal_navigation.py`, `test_player_module.py`, `test_side_ab_frontend.py`, `test_stage_geometry.py`, `test_studio_playlists_frontend.py`, `test_svg_icons.py`.
4. **`tests/integration/` (2 files):**
   - `test_v026_features.py`, `test_v040_features.py`.

---

### Flow 2: Comprehensive Code Quality, Security & Performance Assessment
```
[Assessment Framework]
         │
         ├──► 2.1 Architecture & Design Fit   (Single-node monolith, async workers, state isolation)
         ├──► 2.2 Maintainability              (Modularity, coupling, duplication, file sizing)
         ├──► 2.3 Reliability & Concurrency   (Thread safety, locks, error trapping, job cancellation)
         ├──► 2.4 Efficiency & Performance     (CPU/GPU utilization, audio/video streaming, WebAudio)
         ├──► 2.5 Testability                  (Mocking fidelity, temp path isolation, test determinism)
         ├──► 2.6 Consistency                 (REST standards, Pydantic schemas, DOM event bus contracts)
         └──► 2.7 Readability & Documentation  (Self-documenting code, type hints, docstrings)
         │
         ▼
[Report Generation: tests/ASSESSMENT_REPORT.md]
```

#### Detailed Assessment Matrix:
- **Backend Scope:** `src/main.py`, `src/models.py`, `src/api/routes.py`, `src/services/` (`job_manager.py`, `pipeline.py`, `queue_manager.py`, `playlist_manager.py`, `video_manager.py`, `lrclib_client.py`, `audio_validator.py`, `audio_downloader.py`, `stage1_separator.py`, `stage2_separator.py`).
- **Frontend Scope:** `src/static/` (`app.js`, `player.js`, `karaoke.js`, `library_queue.js`, `playlists.js`, `icons.js`, `index.html`, `styles.css`).
- **Analysis Deliverable:** Structured markdown report at `tests/ASSESSMENT_REPORT.md` answering all 7 questions with quantitative metrics, code snippets, severity ratings (Low, Medium, High), and trade-off analyses.

---

### Flow 3: Architecture & Refactoring Roadmap Plan
```
[Assessment Findings in tests/ASSESSMENT_REPORT.md]
         │
         ▼
[docs/design/ Refactoring Plan & ADR Drafting (Phase 2)]
         ├── Prioritized Technical Debt Backlog
         ├── Component Refactoring Architecture Proposals
         ├── Concurrency & Persistence Hardening Guidelines
         └── Seamless Migration Strategy (Zero Downtime / Zero Regressions)
```

---

## 3. Inputs & Outputs

| Operation | Input | Output / Deliverable |
|---|---|---|
| Test Reorganization | Flat `tests/` directory files | Modular subdirectories (`tests/api/`, `tests/services/`, `tests/frontend/`, `tests/integration/`) + `pytest.ini` / `conftest.py` |
| Quality & Performance Audit | Full source codebase (`src/`, `tests/`, `docs/`) | Detailed evaluation report at `tests/ASSESSMENT_REPORT.md` |
| Refactoring Plan | Audit findings & technical debt matrix | Actionable ADR & refactoring plan in `docs/design/` |

---

## 4. Business & Validation Rules
1. **Zero Test Regressions:** All 194 test cases must pass without alteration to their verification logic.
2. **Pytest Root Invariance:** Running `pytest` from repository root must automatically discover all tests across all subfolders.
3. **Audit Objectivity:** Findings must be evidence-based, citing concrete source lines and architectural trade-offs rather than generic advice.
4. **Backward Compatibility:** No schema changes or breaking changes to `./data/` directories.

---

## 5. Assessment Report Schema (`tests/ASSESSMENT_REPORT.md`)
The output report must adhere to the following structure:
- **1. Executive Summary & Quality Scorecard** (Overview of findings across all 7 dimensions)
- **2. Dimension 2.1: Architecture & Design Fit**
- **3. Dimension 2.2: Maintainability & Code Structure**
- **4. Dimension 2.3: Reliability, Concurrency & Error Resilience**
- **5. Dimension 2.4: Efficiency & System Performance**
- **6. Dimension 2.5: Testability & Suite Architecture**
- **7. Dimension 2.6: Consistency & API/Data Standards**
- **8. Dimension 2.7: Readability, Documentation & Type Safety**
- **9. Prioritized Recommendations & Refactoring Roadmap**

---

## 6. Open Questions
- None. (Scope, directory structure, and evaluation criteria are fully specified).
