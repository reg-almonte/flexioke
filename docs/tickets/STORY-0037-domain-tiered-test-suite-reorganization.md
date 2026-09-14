---
status: approved
approved_by: reg
approved_at: 2026-09-14
implementation: in-review
---

# STORY-0037: Domain-Tiered Test Suite Reorganization & Pytest Invariance

## Parent Epic
- `docs/tickets/EPIC-0012-code-quality-performance-and-test-suite-reorganization.md`

## What it delivers
Eliminates test file clutter by migrating 42+ flat test files in `tests/` into 4 cohesive domain subdirectories (`api/`, `services/`, `frontend/`, `integration/`), while configuring pytest root discovery so `pytest` runs 100% of tests cleanly from the repository root without regressions.

## Acceptance Criteria
- [x] `tests/` flat test files are cleanly migrated to `tests/api/`, `tests/services/`, `tests/frontend/`, and `tests/integration/`.
- [x] `pytest.ini` and `tests/conftest.py` ensure root `pytest` discovery is 100% invariant.
- [x] Running `pytest` from repository root executes all 194+ test cases with zero failures.
- [x] Domain-specific test execution works out of the box (e.g. `pytest tests/api/`, `pytest tests/frontend/`).

## Tasks
- [x] TASK-0076: Migrate Test Files into Domain Subdirectories
- [x] TASK-0077: Pytest Root Invariance Configuration & Fixture Path Resolution

## Blocked by
- None (can start immediately).

## Implementation
- Branch: `story/STORY-0037-domain-tiered-test-suite-reorganization`
- Reorganized 42 test files into `tests/api/`, `tests/services/`, `tests/frontend/`, and `tests/integration/`.
- Created `pytest.ini` and validated 194/194 tests pass cleanly.

