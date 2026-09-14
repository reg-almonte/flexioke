---
status: approved
approved_by: reg
approved_at: 2026-09-14
---

# ADR-0013: Domain-Tiered Test Suite Architecture, Multi-Dimensional Quality Evaluation & Refactoring Strategy

## Context
Over Versions 0.1.0 through 0.4.0, Flexioke has grown into a mature multitrack stem separation and karaoke platform with 194 test cases across 42 test files. All test files currently reside in the flat root of `tests/`, making navigation, targeted test execution, and CI domain slicing cumbersome.

Additionally, as the codebase has expanded across 2-stage AI separation workers, atomic file stores, synchronized WebAudio/LRC engines, background video streaming, and Side A/B dual-track routing, a structured architecture, code quality, security, and performance audit is necessary to identify technical debt, verify reliability/concurrency safety, and plan future architectural refactoring.

## Decision
We adopt **Option 1: Domain-Tiered Subdirectory Layout with Root Pytest Discovery & 7-Point Audit Framework**.

### Key Architectural Decisions:
1. **Domain-Tiered Test Organization (`tests/`):**
   - Restructure `tests/` into 4 dedicated subdirectories:
     - `tests/api/` (12 files): HTTP route handlers, REST contracts, request validation, status codes, and error payloads.
     - `tests/services/` (12 files): Backend services, separation pipeline, background thread managers (`JobManager`, `QueueManager`, `PlaylistManager`, `VideoManager`), atomic stores, and validators.
     - `tests/frontend/` (16 files): Frontend WebAudio gain matrices, DOM element rendering, event bus listeners, SVG icons, and Node.js DOM simulations.
     - `tests/integration/` (2 files): Cross-cutting milestone and end-to-end regression test suites.
   - Configure root `pytest.ini` (`testpaths = tests`) and shared fixtures in `tests/conftest.py` ensuring single-command `pytest` execution from the repository root discovers and executes all 194+ tests seamlessly.
2. **Comprehensive 7-Dimensional Code Quality & Performance Assessment:**
   - Execute a multi-dimensional assessment of backend and frontend source code addressing:
     - 2.1 Architecture & Design Fit
     - 2.2 Maintainability & Decoupling
     - 2.3 Reliability, Concurrency & State Safety
     - 2.4 Efficiency & Performance (Streaming, memory, WebAudio, DOM)
     - 2.5 Testability & Mock Isolation
     - 2.6 Consistency & Standards
     - 2.7 Readability & Documentation Quality
   - Document complete findings, metrics, and risk assessments in `tests/ASSESSMENT_REPORT.md`.
3. **Refactoring & Redesign Roadmap:**
   - Establish a prioritized technical debt remediation roadmap based on the assessment findings, ensuring zero functional regressions and 100% backward compatibility.

## Options Considered

### Option 1: Domain-Tiered Subdirectory Layout with Root Pytest Discovery & 7-Point Audit Framework (Chosen)
- **Pros:**
  - De-clutters `tests/` into clean, navigable domain modules.
  - Enables targeted test runs (`pytest tests/api/`, `pytest tests/services/`, etc.) without losing global root discovery.
  - Generates comprehensive, evidence-based quality audit documentation and refactoring roadmaps.
  - 100% backward compatibility with zero test logic changes.
- **Cons:**
  - Requires moving 40+ files and verifying relative path resolutions for Node.js / HTML test fixtures.

### Option 2: Marker-Based Categorization without Directory Reorganization
- **Pros:**
  - No file movement required.
- **Cons:**
  - Leaves `tests/` root cluttered with 40+ files, failing the primary goal of clean file navigation.

### Option 3: Co-located Feature Slice Architecture (`src/**/tests/`)
- **Pros:**
  - Places tests adjacent to implementation files.
- **Cons:**
  - Pollutes production package directories with test fixtures and Node.js execution scripts; breaks standard Python packaging conventions.

## Consequences
- Pytest configuration in `pytest.ini` and `conftest.py` must support root-level execution and shared fixtures across subdirectories.
- Any test referencing relative paths to `src/static/` or `./data/` must use repository-root relative paths (`Path("src/static/...")`).
- The assessment findings in `tests/ASSESSMENT_REPORT.md` will form the durable foundation for upcoming refactoring and optimization tasks.

## Related
- Functional spec: `docs/specs/version0.4.1.md`
- Requirement: `docs/requirements/version0.4.1.md`
- Supersedes / related ADRs: Extends and complements `docs/design/ADR-0001-stem-separation-player-architecture.md` through `docs/design/ADR-0012-video-backgrounds-stage-geometry-and-side-ab.md`.
