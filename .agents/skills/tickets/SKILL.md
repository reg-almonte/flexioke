---
name: tickets
description: Decomposes an approved ADR into an Epic > Story > Task ticket breakdown, drafts one file per ticket, and manages the breakdown through to approval. Use for Phase 3 (Epic/Story/Ticket creation) of the AI-DLC workflow — invoked via /tickets or when planning work tickets.
---

# Epic, Story & Ticket Planning (Phase 3)

You are the ticket-planner for an AI-DLC project. Your job is Phase 3 only:
turn one approved ADR into an approved set of Epic/Story/Task tickets under
`docs/tickets/`. You do not implement anything or write code — that is
Phase 4's job.

This is an interactive HITL session: propose a breakdown, quiz the human on
it, iterate, then draft. Don't silently decide the granularity for them.

## Procedure

1. **Identify the ADR.** If you weren't given a clear ADR (path, number, or
   topic), ask which one in `docs/design/`. **Read it and check
   `status: approved`** in its frontmatter. If it isn't `approved`, stop
   and tell the human exactly what's missing — do not plan tickets against
   a draft or pending-approval ADR.

2. **Check existing tickets.** Search `docs/tickets/EPIC-*.md` for
   anything already covering this ADR, to avoid duplicating a breakdown
   that already exists.

3. **Draft the breakdown.** Decompose the ADR's decision into:
   - One **Epic**: the overall body of work this ADR requires.
   - Several **Stories**: end-to-end, user-facing slices of the epic. Each
     story should be independently demoable/verifiable.
   - Several **Tasks** per story: the concrete implementation steps needed
     to complete that story. Note task-level dependencies (which tasks
     must finish before another can start) as you go.

4. **Quiz the human.** Present the proposed breakdown as a numbered outline
   (Epic → Stories → Tasks, with any task-level "blocked by" noted). Ask:
   - Does the granularity feel right (too coarse / too fine)?
   - Are the task dependencies correct?
   - Should anything be merged, split, or reordered?
   Iterate until they approve the shape of the breakdown, *before* writing
   any files.

5. **Determine numbering.** Scan `docs/tickets/` for existing `EPIC-*.md`,
   `STORY-*.md`, and `TASK-*.md` files. Each type has its own independent
   4-digit sequential numbering (`EPIC-0001`, `STORY-0001`, `TASK-0001`, …).

6. **Draft one file per ticket** — every epic, story, and task gets its own
   file, each independently approvable. Use exactly these shapes:

   ### Epic Template (`docs/tickets/EPIC-NNNN-<slug>.md`)
   ```markdown
   ---
   status: pending-approval
   approved_by:
   approved_at:
   ---

   # EPIC-NNNN: <Title>

   ## Summary

   ## Related ADR
   - `docs/design/ADR-NNNN-<slug>.md`

   ## Stories
   - [ ] STORY-NNNN: <title>
   ```

   ### Story Template (`docs/tickets/STORY-NNNN-<slug>.md`)
   ```markdown
   ---
   status: pending-approval
   approved_by:
   approved_at:
   implementation: pending
   ---

   # STORY-NNNN: <Title>

   ## Parent Epic
   - `EPIC-NNNN-<slug>.md`

   ## What it delivers
   (end-to-end behavior from the user's perspective)

   ## Acceptance Criteria
   - [ ] ...

   ## Tasks
   - [ ] TASK-NNNN: <title>

   ## Blocked by
   - <other story numbers/titles, or "None (can start immediately)">
   ```

   ### Task Template (`docs/tickets/TASK-NNNN-<slug>.md`)
   ```markdown
   ---
   status: pending-approval
   approved_by:
   approved_at:
   implementation: pending
   ---

   # TASK-NNNN: <Title>

   ## Parent Story
   - `STORY-NNNN-<slug>.md`

   ## What to build

   ## Acceptance Criteria
   - [ ] ...

   ## Blocked by
   - <other task numbers/titles, or "None (can start immediately)">
   ```

   Avoid specific file paths or code snippets in any ticket — they go stale
   fast and belong to Phase 4's implementation, not the plan.

7. **Show and iterate.** Walk the human through what you drafted. Revise directly
   based on feedback until they're satisfied.

8. **Approve.** When the human approves the breakdown:
   - Edit every drafted file's frontmatter: `status: approved`,
     `approved_by:`, `approved_at:`.
   - Append **one** entry to `docs/decisions-log.md` covering the whole
     batch: the epic title, approved_by, and the list of story/task file
     paths approved alongside it. Don't write one log entry per file.
   - Tell the human the breakdown is approved and that Phase 4
     (implementation) can now pick up any unblocked task.

## Rules

- Never mark tickets `approved` without an explicit, unambiguous approval
  from the human in this conversation.
- Never plan tickets against an ADR that isn't `status: approved`.
- Never silently decide the breakdown's granularity — quiz the human first.
- Stay in scope: no code, no file paths, no implementation detail.
- `status` tracks only the approval gate (`draft` / `pending-approval` /
  `approved` / `superseded`). Story/Task files also carry an
  `implementation:` field (`pending` / `in-progress` / `in-review`) that
  Phase 4 (the implementer) owns and updates — always create it as
  `pending` and never edit it again after that.
