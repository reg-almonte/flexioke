---
status: pending-approval
approved_by:
approved_at:
implementation: pending
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
- [ ] `pytest` from root runs all 194+ tests cleanly with 100% pass rate.
- [ ] Subdirectory targeted execution (`pytest tests/api/`, `pytest tests/services/`, etc.) executes without path errors.

## Blocked by
- `TASK-0076`
