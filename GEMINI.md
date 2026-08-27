# software-factory — AI-DLC Project Rules

This repository is set up as an **AI-DLC** (AI-assisted Development Life Cycle)
environment. Development moves through nine phases (plus automated 4.5 and
5.5 review steps), each producing a durable markdown/code artifact that a
human must explicitly approve before the next phase may begin. The full
environment design lives in
[AI-DLC-Setup-Plan.md](AI-DLC-Setup-Plan.md) — read it for rationale; this file
is the operational ruleset Gemini and Antigravity agents must follow day to day.

## Phase map & Skills

| # | Phase | Artifact | Location | Skill |
|---|---|---|---|---|
| — | **Pipeline Dashboard** | Workspace status & next actions | — | `/pipeline` |
| — | **Approval Helper** | Frontmatter update + decisions log | `docs/decisions-log.md` | `/approve` |
| 1 | Requirements Definition (HITL) | requirement doc | `docs/requirements/` | `/requirements` |
| 1 | → Functional Spec (HITL) | functional spec | `docs/specs/` | `/requirements` |
| 2 | Design Creation/Decision (HITL) | ADR | `docs/design/` | `/design` |
| 3 | Epic/Story/Ticket creation | tickets | `docs/tickets/` | `/tickets` |
| 4 | Implementation | code + PR | `src/` | `/implement` |
| 4.5 | PR Review (automated assist) | review findings + PR comment | GitHub PR | `/review-pr` |
| 5 | Test creation (HITL) | tests + check sheet | `tests/`, `docs/checksheets/` | `/write-tests` |
| 5.5 | Check Sheet Review (automated assist) | completeness review | `docs/checksheets/` | `/review-checksheet` |
| 6 | Test Execution | bug report | `docs/bugs/` | `/run-tests` |
| 7 | Bug-fixing (HITL) | fix diff | `src/` | `/bugfix` |
|   | → Test ↔ Bugfix Loop | clean test run | `docs/bugs/` | `/fix-until-green` |
| 8 | Local deployment (light HITL) | running local process | — | `/deploy-local` |
| 9 | Release (HITL) | release manifest | `docs/releases/` | `/release` |

## Tiered Lifecycle Speeds

Not every task requires the full 9-phase ceremony. Three operational paths are supported:

1. **Full Path (Phases 1 → 9):** Required for new features, major architecture changes, and public APIs. Follows the full sequence from requirements interview to release manifest.
2. **Fast-Track Bugfix (Phases 6 ↔ 7):** For bugs reported in existing code. Run `/bugfix <bug-slug>` or loop with `/fix-until-green <story-id>`. Fixed only after an actual clean Phase 6 test execution.
3. **Direct Task / Chore (Phases 3 → 4.5):** For maintenance, chores, or minor refactoring covered by existing architecture decisions. Plan a task ticket, implement via `/implement`, and review via `/review-pr`.

## The one hard rule: no phase without an approved predecessor

Every artifact in `docs/requirements/`, `docs/specs/`, `docs/design/`,
`docs/tickets/`, `docs/checksheets/`, and `docs/releases/` carries a YAML
frontmatter status header at the very top of the file (`docs/bugs/` is the
one exception — see below):

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by:
approved_at:
---
```

- The agent must **never** start work that depends on an artifact whose status is
  not `approved`. If asked to, say so and point at what's missing instead of
  proceeding.
- The agent may draft an artifact and set it to `pending-approval`, but only a
  human flips it to `approved` (by editing the file, telling the agent, or using `/approve`).
- Every approval — requirements, design, ticket scope, and especially a
  release — gets one line appended to `docs/decisions-log.md` (what was
  approved, by whom, when). Use the `/approve` skill for automated, consistent logging.
- Story/Task tickets also carry an `implementation:` frontmatter field
  (`pending` / `in-progress` / `in-review`), owned by Phase 4 (the
  implementer) once the ticket is approved. This tracks build progress
  separately from the `status:` approval gate — approval never changes
  once granted; `implementation` does, as work proceeds.
- `docs/bugs/` reports are the one artifact type without the approval
  gate: Phase 6 (the tester) files them directly (`status: open`) since
  filing one is an objective observation, not a decision. The human
  approval gate for a bug lives in Phase 7, over the proposed fix.

## Permissions & HITL enforcement

- Default operation for this project follows **plan mode** / interactive review.
  The agent presents a plan and gets explicit approval before making modifications
  or applying major changes across all phases.
- This tool never deploys to production or contacts real infrastructure.
  Phase 9 (`/release`) packages a release manifest and, once a human
  approves it, tags the release — the same convention-based approval gate
  as every other phase. Carrying out the actual deployment is always the
  human's (or their separate ops process's) action, never the agent's.

## Working conventions & Branching

- **Story-Branch Flow:** For multi-task stories, all tasks accumulate on a parent branch
  named `story/STORY-NNNN-<slug>`. Inline TDD, integration tests (Phase 5), and check sheet
  verifications run against this branch. Once clean, a single cohesive PR is opened against `main`.
- **Task / Bugfix Branch:** Standalone tasks or bugfixes operate on `task/TASK-NNNN-<slug>`
  or `bugfix/<slug>` branches, never directly on `main`.
- General rule: never commit or push unless explicitly asked.
  **Scoped exception for Phases 4 and 7**: the implementer and bug-triager
  may commit, push a feature/story branch, and open/update a PR without being asked
  first — a PR is a review gate, not a merge, so nothing lands without a human.
  This exception never extends to pushing directly to the default/protected branch
  or to merging a PR; that always requires an explicit human action.
- **Phase 6 ↔ 7 loop:** `/fix-until-green <story-or-epic>` alternates the
  tester and bug-triager automatically (re-testing after each approved fix)
  until a clean run, with no iteration cap — it keeps going until clean or
  a human interrupts it. This automates the *re-testing*, not the
  *approval*: bug-triager still stops for explicit human approval before
  applying any fix, every round. Only Phase 6, by actually running clean,
  flips a bug report to `status: fixed` — bug-triager never does this
  itself, even after applying a fix it believes is correct.
- This is a scaffolding-stage repo: no language/framework has been chosen
  yet. Do not assume a tech stack — that decision belongs to Phase 1/2 for
  the first real feature.

## Agent Skills & Discovery

Lifecycle capabilities are organized as Antigravity skills located in
`.agents/skills/`. Run `/pipeline` at any time to inspect active progress and
receive recommendations on what command to run next.

### Issue tracker

Issues live in this repo's GitHub Issues (repo inferred via `git remote -v`), using the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout: one `CONTEXT.md` and `docs/design/` at the repo root. See `docs/agents/domain.md`.
