# AI-DLC Environment Setup Plan (Google Gemini & Antigravity)

> AI-DLC = AI-assisted Development Life Cycle. Every phase below is designed as a
> **Human-in-the-Loop (HITL)** checkpoint: Gemini and Antigravity agents propose, draft, and execute;
> a human reviews, edits, and explicitly approves before the next phase unlocks.

## 1. Goals & Principles

- Cover the full lifecycle: **Requirements → Functional Spec → Design → Tickets → Implementation → PR Review → Tests + Check Sheet → Check Sheet Review → Test Execution → Bug-fixing → Local Deploy → Release.**
- Every phase produces a durable, human-readable artifact (markdown doc, ADR, ticket file, PR) that the next phase consumes — this is the audit trail and the thing a human actually reviews.
- HITL is enforced structurally, not just by convention: plan-mode pauses and explicit approval markers in files gate every phase. This tool never touches real production infrastructure — Phase 9 packages a release for a human to actually deploy, it doesn't deploy anything itself.
- High developer ergonomics: automated status tracking via `/pipeline`, frictionless batch approvals via `/approve`, and clean Story-branch integration workflows.

### Antigravity & Gemini building blocks used

| Building block | Purpose here |
|---|---|
| `GEMINI.md` | Project-wide house rules, phase map, HITL policy, tiered lifecycle speeds |
| `.agents/skills/<skill-name>/SKILL.md` | Modular on-demand skills per lifecycle role & helper (pipeline, approve, requirements, design, tickets, implement, review-pr, write-tests, review-checksheet, run-tests, bugfix, fix-until-green, deploy-local, release) |
| Slash commands | Command entry points (`/pipeline`, `/approve`, `/requirements`, `/design`, `/tickets`, `/implement`, `/write-tests`, `/run-tests`, `/bugfix`, `/fix-until-green`, `/deploy-local`, `/release`) |
| Git branches / worktrees | Isolate implementation/bugfix work per story or ticket without touching a human's in-progress branch |

## 2. Repository Skeleton

```
software-factory/
├── GEMINI.md
├── .agents/
│   └── skills/
│       ├── pipeline/            # Phase navigation & status dashboard
│       │   └── SKILL.md
│       ├── approve/             # Frontmatter + audit logger helper
│       │   └── SKILL.md
│       ├── requirements/        # Phase 1: Requirements & spec interview
│       │   └── SKILL.md
│       ├── design/              # Phase 2: Solution architecture & ADRs
│       │   └── SKILL.md
│       ├── tickets/             # Phase 3: Ticket decomposition
│       │   └── SKILL.md
│       ├── implement/           # Phase 4: TDD & automated PR review dispatch
│       │   └── SKILL.md
│       ├── review-pr/           # Phase 4.5: Isolated PR review
│       │   └── SKILL.md
│       ├── write-tests/         # Phase 5: Integration tests & checksheet
│       │   └── SKILL.md
│       ├── review-checksheet/   # Phase 5.5: Isolated checksheet review
│       │   └── SKILL.md
│       ├── run-tests/           # Phase 6: Test execution & bug filing
│       │   └── SKILL.md
│       ├── bugfix/              # Phase 7: Bug triaging & fix proposal
│       │   └── SKILL.md
│       ├── fix-until-green/     # Phase 6 ↔ 7 test-fix loop
│       │   └── SKILL.md
│       ├── deploy-local/        # Phase 8: Local deploy & healthcheck
│       │   └── SKILL.md
│       └── release/             # Phase 9: Release manifest & tagging
│           └── SKILL.md
├── docs/
│   ├── requirements/            # one file per requirement/feature request
│   ├── specs/                   # functional specs (Phase 1's final output)
│   ├── design/                  # ADRs + architecture docs
│   ├── tickets/                 # epics/stories/tasks
│   ├── checksheets/             # QA verification checklists (Phase 5)
│   ├── bugs/                    # bug reports filed by Phase 6 (no approval gate)
│   ├── releases/                # release manifests (Phase 9)
│   └── decisions-log.md         # append-only HITL decision trail
├── src/
└── tests/
```

Each markdown artifact carries a small status header, e.g.:

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by:
approved_at:
---
```

This is the mechanism that makes "approved" checkable by both humans and Gemini (the agent refuses to proceed off a doc that isn't `approved`).

## 3. Tiered Lifecycle Speeds

1. **Full Path (Phases 1 → 9):** New features, significant architecture changes, or major refactors.
2. **Fast-Track Bugfix (Phases 6 ↔ 7):** Target open bug reports directly with `/bugfix` or `/fix-until-green`.
3. **Direct Task / Chore (Phases 3 → 4.5):** Minor tasks or maintenance covered by existing ADRs.

## 4. Phase-by-Phase Plan

### Phase 0 — Foundation & Dashboard

- `GEMINI.md`: project purpose, phase map, the HITL rule ("never start phase N+1 work off an artifact that isn't `status: approved`"), coding conventions.
- `/pipeline`: interactive dashboard displaying current progress, unblocked tasks, and next recommended command.
- `/approve`: helper to batch-approve documents and tickets while updating `docs/decisions-log.md`.

### Phase 1 — Requirements Definition (HITL)

- **Skill** `requirements` (`.agents/skills/requirements/SKILL.md`), two stages:
  - **Stage A:** interviews the human, drafts `docs/requirements/<feature>.md` (problem, goals, non-goals, acceptance criteria), sets `status: pending-approval`.
  - **Stage B (Functional Spec), only once Stage A is approved:** interviews further for behavioral detail (flows, inputs/outputs, business rules) and drafts `docs/specs/<feature>.md` — this is Phase 1's final output, and what Phase 2 actually gates on.
- **Command** `/requirements <topic>`.
- **HITL gate:** human edits either doc directly or runs `/approve <doc>` — once for requirements, again for the functional spec.

### Phase 2 — Design Creation / Decision (HITL)

- **Skill** `design` (`.agents/skills/design/SKILL.md`): reads the approved functional spec, proposes 1–3 design options with trade-offs, writes an ADR to `docs/design/ADR-NNNN-<slug>.md`.
- **HITL gate:** human selects an option; ADR moves to `status: approved`.

### Phase 3 — Epic/Story/Ticket Creation

- **Skill** `tickets` (`.agents/skills/tickets/SKILL.md`): decomposes the approved ADR into an Epic → Stories → Tasks breakdown in `docs/tickets/`, one file per ticket, each with acceptance criteria and traceability links.
- **HITL gate:** human reviews the breakdown's granularity and dependencies; approves via `/approve EPIC-NNNN --all`.

### Phase 4 — Implementation & Story-Branch Integration

- **Skill** `implement` (`.agents/skills/implement/SKILL.md`): takes one approved Task at a time, works on a `story/STORY-NNNN-<slug>` branch (or `task/TASK-NNNN-<slug>`), implements using inline TDD, commits, and opens a PR.
- **Phase 4.5 Isolated Subagent Review:** Automatically delegates to an isolated subagent running `/review-pr` upon PR opening.
- **HITL gate:** human reviews the PR diff and automated review findings before merging.

### Phase 5 — Test Creation & Check Sheet

- **Skill** `write-tests` (`.agents/skills/write-tests/SKILL.md`): writes integration/end-to-end tests across the Story, then drafts a QA check sheet at `docs/checksheets/<slug>.md`.
- **Phase 5.5 Isolated Check Sheet Review:** Automatically delegates to an isolated subagent running `/review-checksheet`.
- **HITL gate:** human confirms coverage and approves check sheet via `/approve`.

### Phase 6 — Test Execution

- **Skill** `run-tests` (`.agents/skills/run-tests/SKILL.md`): runs the test suite against the Story branch, checks off items in the check sheet execution log, and files consolidated bug reports for any failures (`docs/bugs/<slug>.md`).

### Phase 7 — Bug-Fixing (HITL)

- **Skill** `bugfix` (`.agents/skills/bugfix/SKILL.md`): root-causes failures, proposes fixes, applies approved fixes on the branch, and pushes updates.
- **Phase 6 ↔ 7 Loop:** `/fix-until-green <story-id>` alternates test execution and bug fixing until a clean run is verified.

### Phase 8 — Local Deployment (light HITL)

- **Skill** `deploy-local` (`.agents/skills/deploy-local/SKILL.md`): discovers project start scripts, installs dependencies, handles placeholder config, starts local processes, and verifies health.

### Phase 9 — Release (HITL)

- **Skill** `release` (`.agents/skills/release/SKILL.md`): packages release manifest at `docs/releases/<version>.md` with pre-deployment checklist, and creates git tag only upon human approval.

## 5. Skill / Slash Command Summary

| Command | Phase | Description |
|---|---|---|
| `/pipeline` | Dashboard | Status dashboard & next recommended action |
| `/approve <target>` | Gate Helper | Approve doc or batch tickets & update decisions log |
| `/requirements <topic>` | 1 (both stages) | Requirements doc & functional spec interview |
| `/design <spec>` | 2 | Propose architecture options & draft ADR |
| `/tickets` | 3 | Decompose ADR into Epic → Stories → Tasks |
| `/implement <task-id>` | 4 (+4.5 auto) | Inline TDD on Story branch & automated PR review |
| `/review-pr <pr>` | 4.5 | Isolated PR review (standards, spec, suspicious code) |
| `/write-tests <story-id>` | 5 (+5.5 auto) | Integration tests & QA check sheet |
| `/review-checksheet <slug>` | 5.5 | Check sheet completeness & coverage review |
| `/run-tests <story-id>` | 6 | Execute test suite & check sheet, file bugs |
| `/bugfix <bug-slug>` | 7 | Root-cause open bug & propose fix |
| `/fix-until-green <story-id>` | 6+7 loop | Loop testing and bug fixing until green |
| `/deploy-local` | 8 | Setup, start, and health-check local instance |
| `/release <version>` | 9 | Package release manifest & tag upon approval |
