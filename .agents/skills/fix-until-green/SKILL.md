---
name: fix-until-green
description: Loop Phase 6 (test execution) and Phase 7 (bug-fixing) for a Story/Epic until a clean run — each fix still needs user approval (AI-DLC Phase 6+7 loop). Use when running /fix-until-green.
---

# Fix Until Green Loop (Phase 6 ↔ Phase 7)

Run this workflow to iterate testing and bug fixing until all tests pass cleanly.
Every bug-triager pass needs the human's approval before it applies
anything, and the human should see each round's result before the next one
starts. There is deliberately **no iteration cap** — keep looping until a
clean run or until the human interrupts.

## Scope
Identify which Story/Epic in `docs/tickets/` to verify and fix.

## Loop Procedure

1. **Execute Tests (Phase 6):** Run the `/run-tests` procedure for this scope.
   On the **first** pass, test the current checkout normally. On every pass
   **after** a `bugfix/<slug>` branch has been created (i.e., after step 3 has
   run at least once), verify that branch instead.

2. **Check Status:**
   - If tests report clean (bug report closed as `fixed`, or no bug report was ever needed):
     **Stop the loop.** Inform the user that the run is clean, and if a `bugfix/<slug>`
     branch/PR was created, point them at it as ready for review/merge.
   - If failures exist (`open`/`in-progress` bug report exists): proceed to Step 3.

3. **Triage and Fix (Phase 7):** Run the `/bugfix` procedure against the open bug report.
   Present root causes and proposed fixes, and wait for explicit human approval before
   applying any changes.

4. **Iterate:** Once fixes are applied and pushed (or the user deferred/declined some),
   loop back to Step 1.

Between rounds, briefly inform the user which round is running and what changed,
keeping the loop visible and interactive.
