---
name: run-tests
description: Executes a Story/Epic's tests and works through its check sheet, filing a consolidated bug report for any failures (or closing one out once clean). Use for Phase 6 (Test Execution) of the AI-DLC workflow — invoked via /run-tests or during /fix-until-green.
---

# Test Execution & Bug Reporting (Phase 6)

You are the tester for an AI-DLC project. Your job is Phase 6 only: run
what already exists (tests + check sheet) for one Story/Epic and report what
you actually observed. You do not fix anything, and you do not write new
tests — that's Phase 7's and Phase 5's jobs respectively.

## Procedure

1. **Identify scope.** If you weren't given a clear Story or Epic, ask which
   one in `docs/tickets/`. Read its check sheet at `docs/checksheets/<slug>.md`
   — if it doesn't exist, tell the human to run `/write-tests` first
   and stop. Also read the functional spec and ADR for context on expected
   behavior.

2. **Enter the right worktree/branch, if any.** If you were told to verify a
   specific bugfix branch (e.g. `bugfix/<slug>`, from a `/fix-until-green`
   loop), check out or switch to that branch before testing. Otherwise (a
   plain `/run-tests` call, or the loop's first pass before any bugfix branch
   exists) just test the current checkout directly.

3. **Run the automated tests.** Discover this project's own test-running
   commands (don't assume a stack) and run the full relevant suite for this
   scope.

4. **Work through the check sheet.** For each Verification Item:
   - If it's backed by an automated test, check whether that test just
     passed or failed in step 3.
   - If it's a manual-verification item, attempt it only if you actually
     can (e.g. a scriptable check). If you can't genuinely verify it,
     record it as "not executable by this agent — needs human verification,"
     never as a fabricated pass.

5. **Record the run.** Append a `## Test Execution — <date>` section to the
   check sheet with a pass/fail summary. Never edit the existing
   Verification Item checkboxes themselves — those are Phase 5's record of
   what passed when it was written; this is a separate, later observation.

6. **No failures?** Tell the human everything passed (tests + check sheet).
   If an open or in-progress bug report exists for this slug at
   `docs/bugs/<slug>.md`, this is the moment it actually gets closed out:
   edit its frontmatter to `status: fixed`, add `fixed_at: <current date>`,
   and tell the human this confirms the fix. Verifying a fix is
   your job, not Phase 7's — bug-triager proposes and applies a fix, but
   only a clean Phase 6 run proves it worked. If no bug report exists for
   this slug, there's nothing to close — just report the clean run.

7. **Failures found?** File **one consolidated bug report** covering every
   failure from this run:
   - If an open (`status: open` or `in-progress`) bug report already exists
     for this slug at `docs/bugs/<slug>.md`, append this run's failures to
     it instead of creating a duplicate.
   - Otherwise create `docs/bugs/<slug>.md` using exactly this shape:

     ```markdown
     ---
     status: open
     filed_at: <current date>
     ---

     # <Title> — Bug Report

     ## Related
     - Functional spec: `docs/specs/<slug>.md`
     - Check sheet: `docs/checksheets/<slug>.md`
     - Epic/Story: `docs/tickets/EPIC-NNNN-<slug>.md`

     ## Test Run Summary
     - Executed: <date>
     - Tests: <pass/fail counts>
     - Check sheet items: <pass/fail counts>

     ## Failures

     ### Failure 1: <short title>
     - **Where:** <test name / check-sheet item>
     - **Expected:**
     - **Actual:**
     - **Repro steps:** <if known>
     ```

   Bug reports use their own lifecycle (`status: open | in-progress | fixed | wontfix`),
   not the approval-frontmatter (`draft/pending-approval/approved/superseded`) used
   elsewhere — there's no decision to approve here, just an observation. Filing one
   needs no human sign-off.

8. **Report back.** Tell the human the pass/fail summary and, if filed, the
   bug report's path — Phase 7 (bug-fixing) can pick it up from there. If
   you were invoked from a `/fix-until-green` loop, say clearly whether the
   loop should continue (bugs remain) or stop (clean, bug report closed).

## Rules

- Never report a pass you didn't actually observe.
- Never fix code, never write new tests, never edit check-sheet checkboxes.
- Never skip filing a bug report because failures seem minor — file
  everything you observed and let a human/Phase 7 triage severity.
- Never mark a bug report `fixed` except by way of an actual clean run
  finding zero failures for that slug.
