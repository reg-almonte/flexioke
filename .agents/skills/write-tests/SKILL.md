---
name: write-tests
description: Writes integration/end-to-end tests beyond inline TDD, produces a QA check sheet mapping spec/design items to verification checks, and manages it through to approval. Use for Phase 5 (Test Creation) of the AI-DLC workflow — invoked via /write-tests.
---

# Test Creation & Check Sheet Authoring (Phase 5)

You are the test-author for an AI-DLC project. Your job is Phase 5: cover
what Phase 4's per-task inline TDD didn't (broader integration/end-to-end
behavior across a Story or Epic), and produce a QA check sheet at
`docs/checksheets/<slug>.md` mapping every functional-spec/design item to a
verification check. You do not implement features — that's Phase 4's job.

## Procedure

1. **Identify scope.** If you weren't given a clear Story or Epic, ask
   which one in `docs/tickets/`. Read it, its parent chain up to the
   functional spec (`docs/specs/`) and ADR (`docs/design/`), and its child
   tasks. Check each relevant Task's `implementation:` field — if any is
   still `pending`/`in-progress`, warn the human that there's nothing yet
   to integration-test for that task and ask whether to proceed on the rest.

2. **Find the gap.** Look at what tests already exist (per-task tests
   written during Phase 4's inline TDD). Don't duplicate unit-level
   coverage that's already there — focus on integration/end-to-end paths
   that only make sense across multiple tasks, and any acceptance criteria
   at the Story/Epic level that no single task's tests actually exercise.

3. **Write the tests.** Follow behavioral testing: tests verify
   behavior through public interfaces, not internals. Discover this
   project's own test-running commands rather than assuming a stack.

4. **Run them.** Run the new tests (and re-run the full suite) so you know
   which items actually pass right now.

5. **Draft the check sheet.** Enumerate every verifiable item from the
   functional spec's flows/business rules, the ADR's decision/consequences,
   and the Epic/Stories' acceptance criteria. Write
   `docs/checksheets/<kebab-case-slug>.md` (same slug as the feature) using
   exactly this shape:

   ```markdown
   ---
   status: pending-approval
   approved_by:
   approved_at:
   ---

   # <Title> — Check Sheet

   ## Related
   - Functional spec: `docs/specs/<slug>.md`
   - ADR: `docs/design/ADR-NNNN-<slug>.md`
   - Epic: `docs/tickets/EPIC-NNNN-<slug>.md`

   ## Verification Items

   - [ ] <item> — verified by: <test file/name, or "manual: <how to check>">
   ```

   Check off (`- [x]`) any item whose backing automated test you just ran
   and confirmed passes. Leave unchecked anything that fails, has no
   automated coverage yet, or needs manual verification — and say so next
   to the item rather than checking it optimistically.

6. **Show and iterate.** Walk the human through the check sheet and what it
   covers. Revise directly based on feedback.

7. **Trigger Phase 5.5 Check Sheet Review (Isolated Subagent).**
   Immediately delegate an automated completeness review to an isolated subagent
   running the `/review-checksheet` skill against the newly drafted check sheet.
   The subagent will independently cross-reference the check sheet against the functional spec,
   ADR, and tickets, append its findings section, and return the summary.

8. **Approve.** Present the drafted check sheet and the Phase 5.5 completeness review findings
   to the human. When the human explicitly approves:
   - Edit the frontmatter: `status: approved`, `approved_by:`,
     `approved_at:`.
   - Append one entry to `docs/decisions-log.md`.
   - Tell the human it's approved and where it lives.

## Rules

- Never check off a verification item without having actually run its
  backing test and seen it pass.
- Never invent spec/design items or acceptance criteria that aren't
  actually in the functional spec, ADR, or tickets.
- Never mark the check sheet `approved` without explicit human approval.
- Stay in scope: no new features, no design changes.
