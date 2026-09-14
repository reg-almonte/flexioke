---
status: approved
approved_by: reg
approved_at: 2026-09-14
implementation: in-review
---

# TASK-0080: Formulate Architectural Refactoring Decisions & Technical Debt Backlog

## Parent Story
- `docs/tickets/STORY-0039-architectural-refactoring-roadmap.md`

## What to build
Formulate a concrete architectural refactoring plan based on `tests/ASSESSMENT_REPORT.md`:
- Prioritized backlog of refactoring targets (e.g. modularizing `player.js` / `karaoke.js`, centralized state store, unified error handler).
- Step-by-step implementation guide detailing test-driven refactoring without behavioral breaking changes.
- Document plan in `docs/design/` to prepare the foundation for Version 0.4.2 / 0.5.0 implementation.

## Acceptance Criteria
- [x] Refactoring plan and technical debt backlog formulated in `docs/design/`.
- [x] Clear milestones and zero-regression migration strategies defined.

## Blocked by
- `TASK-0079`

## Implementation
- Branch: `story/STORY-0039-architectural-refactoring-roadmap`
- Authored `docs/design/REFACTORING_ROADMAP.md` covering API router decomposition (REF-01), frontend modularization (REF-02), event bus decoupling (REF-03), parameter aliasing (REF-04), SSE progress streaming (REF-05), and state store unification (REF-06).

