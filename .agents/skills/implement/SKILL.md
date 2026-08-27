---
name: implement
description: Implements an approved Task using inline TDD on a dedicated task/story branch, commits, and prepares a PR with automated isolated PR review. Use for Phase 4 (Implementation) of the AI-DLC workflow — invoked via /implement or when implementing tasks.
---

# Task Implementation & TDD (Phase 4)

You are the implementer for an AI-DLC project. Your job is Phase 4 only:
turn one approved Task into working code on a dedicated branch with an open
PR. You do not write the ticket, and you do not merge anything — merging is
always the human's decision.

## Procedure

1. **Identify the task.** If you weren't given a clear Task (path, number,
   or topic), ask which one in `docs/tickets/`. Prefer Task-level tickets
   (the atomic implementation unit); if only a Story with no tasks exists,
   confirm with the human before implementing at Story granularity.

2. **Read the chain.** Read the Task, its parent Story, parent Epic, and
   the Story/Epic's related ADR and requirement doc. Check the Task's
   `status: approved` in frontmatter — if it isn't, stop and tell the human
   what's missing. Also read `CONTEXT.md` and relevant ADRs in
   `docs/design/` per `docs/agents/domain.md`'s consumer rules, if they
   exist, so your work uses the project's own vocabulary and respects prior
   decisions.

3. **Check blockers.** Read the Task's "Blocked by" list. For each blocker,
   check its `implementation:` field. If any blocker isn't at least
   `in-review` or merged, warn the human and ask whether to proceed anyway.

4. **Claim it.** Edit the Task's frontmatter: `implementation: in-progress`.

5. **Branching Strategy (Story vs. Task Branch):**
   - **Story-Branch Flow (Recommended for multi-task stories):** Switch to or create
     the parent Story branch `story/STORY-NNNN-<slug>`. All tasks under this Story
     accumulate on this branch.
   - **Task-Branch Flow (Standalone):** Create a fresh branch `task/TASK-NNNN-<slug>`.
   Do all implementation work on the branch, never directly in `main`.

6. **Implement with inline TDD.** Follow test-driven development:
   agree the seams, red before green, one slice at a time. Write
   the task's tests and code together in small increments against its
   Acceptance Criteria — don't write all the code first and backfill tests.

7. **Verify.** Discover this project's own build/typecheck/test commands
   (check `package.json` scripts, `Makefile`, or whatever this repo
   actually uses — never assume a stack). Run typechecking and the
   relevant tests as you go, and the full test suite once before finishing.

8. **Commit.** Once the Task's Acceptance Criteria are met, commit the work
   to the branch. Commit messages should reference the Task
   (e.g. `TASK-NNNN: <summary>`).

9. **Push and open a PR:**
   - Push the branch to `origin` (never directly to `main`).
   - If this is a standalone Task branch, or the final Task completing a Story branch,
     open a PR (e.g. via `gh pr create`) linking the Task/Story, parent Epic, and related ADR.
   - If additional tasks in the Story remain pending on the Story branch, you may defer the PR
     or open a draft PR.

10. **Mark in-review.** Edit the Task's frontmatter: `implementation: in-review`.
    Add an `## Implementation` section to the Task file with the branch name
    and PR URL/number.

11. **Trigger Phase 4.5 PR Review (Isolated Subagent).**
    If a PR was opened, immediately delegate an automated review to an isolated subagent
    running the `/review-pr` skill against the newly opened PR (passing the PR number and Task path).
    The subagent will inspect the diff with a clean, unbiased context, post review
    findings as a comment on GitHub, and return the findings summary.

12. **Report back.** Present the Task path, branch name, PR number/URL, and the
    summary of findings from the automated PR review. Recommend the next step (e.g.
    next task in story, or `/write-tests <story-id>`).

## Rules

- Never implement against a Task that isn't `status: approved`.
- Never push to the default/protected branch directly, and never merge a
  PR yourself — that's always the human's call.
- Never skip straight to "done." This skill's terminal state is
  `in-review`; a human marks a task fully done after the PR is actually merged.
- Stay in scope: don't redesign the ADR or rewrite the ticket's scope
  mid-implementation.
