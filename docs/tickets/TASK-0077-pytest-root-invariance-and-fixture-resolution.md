---
status: approved
approved_by: reg
approved_at: 2026-09-14
implementation: in-review
---

# TASK-0077: Pytest Root Invariance Configuration & Fixture Path Resolution

## Parent Story
- `docs/tickets/STORY-0037-domain-tiered-test-suite-reorganization.md`

## What to build
Configure pytest root discovery and fix any path-dependent fixtures:
- Create or update `pytest.ini` with `testpaths = tests` and python path configurations.
- Verify and standardize any Node.js simulation tests or HTML file readers to use repository-root relative paths (`Path("src/static/...")`).
- Verify all 194 test cases pass when running `pytest` from repo root as well as domain subdirectories (`pytest tests/api/`, etc.).

## Acceptance Criteria
- [x] `pytest` from root runs all 194+ tests cleanly with 100% pass rate.
- [x] Subdirectory targeted execution (`pytest tests/api/`, `pytest tests/services/`, etc.) executes without path errors.

## Blocked by
- `TASK-0076`

## Implementation
- Branch: `story/STORY-0037-domain-tiered-test-suite-reorganization`
- Created `pytest.ini` defining `testpaths = tests` and `pythonpath = .`.
- Updated static path resolution in `tests/frontend/test_svg_icons.py` and `tests/frontend/test_karaoke_cinema_fullscreen.py` to reference repo root via `parents[2]`.
- Verified 194/194 tests pass cleanly across root and all 4 subdirectories.

