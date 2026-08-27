---
name: pipeline
description: Inspects workspace artifacts, git branches, and PR status; displays an end-to-end AI-DLC pipeline dashboard and recommends the exact next action. Use when checking project status or running /pipeline.
---

# AI-DLC Pipeline & Status Dashboard

Inspect the current workspace status across all AI-DLC phases, summarize approved vs. pending artifacts, identify open blockers, and recommend the exact next command for the developer.

## Procedure

1. **Scan Artifacts in `docs/`:**
   - **Requirements:** Check `docs/requirements/*.md` for draft, pending-approval, or approved documents.
   - **Specs:** Check `docs/specs/*.md` for draft, pending-approval, or approved functional specs.
   - **Design (ADRs):** Check `docs/design/ADR-*.md` for draft, pending-approval, approved, or superseded ADRs.
   - **Tickets:** Check `docs/tickets/` for Epics, Stories, and Tasks:
     - Check `status:` (`pending-approval` vs `approved`)
     - Check `implementation:` (`pending`, `in-progress`, `in-review`)
     - Check `Blocked by:` dependencies to identify which tickets are immediately ready to build.
   - **Check Sheets:** Check `docs/checksheets/*.md` and their latest `## Test Execution` or `## Completeness Review` results.
   - **Bugs:** Check `docs/bugs/*.md` for `open` or `in-progress` bug reports.
   - **Releases:** Check `docs/releases/*.md` for release manifests.

2. **Check Git & Branch Status:**
   - Current branch name (`git branch --show-current`).
   - Active feature/story/bugfix branches.
   - Open PRs via `gh pr list` (if `gh` CLI is authenticated and available).

3. **Render Pipeline Dashboard:**
   Present a clear, structured dashboard summarizing:
   - **Active Stream / In-Progress Feature:** Name of the active Epic/Story.
   - **Phase Gate Summary:** Status of Requirements → Spec → ADR → Tickets → Code → Tests → Release.
   - **Unblocked Tasks:** Which approved Tasks can be picked up immediately.
   - **Open Pull Requests:** PR number, branch, review findings, and merge status.
   - **Active Bugs:** Summary of open bug reports in `docs/bugs/`.

4. **Recommend Next Action:**
   Provide the single, most relevant next step with the exact command to run:
   - If a doc is `pending-approval`: Suggest `/approve <doc-path>` or reviewing the draft.
   - If tickets are approved and unblocked: Suggest `/implement <task-id>`.
   - If a PR is open and reviewed: Suggest reviewing/merging the PR.
   - If code is ready for testing: Suggest `/write-tests <story-id>` or `/run-tests <story-id>`.
   - If bugs are open: Suggest `/bugfix <bug-slug>` or `/fix-until-green <story-id>`.
   - If all stories are green: Suggest `/deploy-local` or `/release <version>`.

## Example Dashboard Output

```text
============================================================
              AI-DLC PIPELINE STATUS BOARD
============================================================
Active Feature: User Authentication (EPIC-0001)

[Phases 1-2] Requirements & Design
  ✓ docs/requirements/user-auth.md (Approved by alice)
  ✓ docs/specs/user-auth.md        (Approved by alice)
  ✓ docs/design/ADR-0001-jwt.md    (Approved by alice)

[Phase 3] Tickets (EPIC-0001)
  ✓ STORY-0001: JWT Generation & Sign-in (Approved)
    ├── TASK-0001: Token Signing Utility [in-review] (PR #4 - Review clean)
    └── TASK-0002: Login HTTP Handler     [pending]   (Blocked by TASK-0001)

[Phases 5-7] Testing & Quality
  • Check Sheet: docs/checksheets/user-auth.md (Pending integration tests)
  • Open Bugs: None

------------------------------------------------------------
>> NEXT RECOMMENDED ACTION:
Review and merge PR #4 on GitHub, then run:
`/implement TASK-0002`
============================================================
```
