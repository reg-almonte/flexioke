---
name: approve
description: Automates approving an AI-DLC document or a batch of tickets, updating YAML frontmatter to 'status: approved' and logging an audit entry in docs/decisions-log.md. Use when approving artifacts or running /approve.
---

# Document & Ticket Batch Approval Helper

Automates the Human-in-the-Loop (HITL) approval ceremony by updating artifact frontmatter and recording an audit trail in `docs/decisions-log.md`.

## Arguments

- `/approve <path-or-slug>`: Approves a specific document (e.g. `docs/requirements/user-auth.md`, `docs/specs/user-auth.md`, `docs/design/ADR-0001-jwt.md`, `docs/checksheets/user-auth.md`, `docs/releases/v1.0.0.md`).
- `/approve EPIC-NNNN --all`: Approves an Epic and all of its associated child Stories and Tasks in one pass.
- `/approve STORY-NNNN --all`: Approves a Story and all of its child Tasks.
- `/approve <ticket-id>`: Approves a single Story or Task ticket.

## Procedure

1. **Verify Target Artifact(s):**
   - Resolve the target file(s) from arguments or ask the human if ambiguous.
   - Read the target file(s) and inspect the current frontmatter.
   - If already `approved`, inform the user that it is already approved.

2. **Confirm Approval with the Human:**
   - Briefly state what is being approved (e.g. *"Approving EPIC-0001 with 2 child Stories and 5 Tasks"*).
   - Obtain user identifier (e.g. git author name, email, or username) and current date.

3. **Update Frontmatter:**
   For each target file, update the YAML frontmatter:
   ```yaml
   ---
   status: approved
   approved_by: <user>
   approved_at: <current-session-date>
   ---
   ```
   *(Preserve existing fields such as `implementation:` if present in Story/Task tickets).*

4. **Record in Decisions Log:**
   Append a clean entry to `docs/decisions-log.md` matching the established format:
   - For single files:
     ```markdown
     - date: <YYYY-MM-DD>
       artifact: <file-path>
       approved_by: <user>
       notes: <brief summary of decision or approved spec>
     ```
   - For batch approvals (Epics/Stories):
     ```markdown
     - date: <YYYY-MM-DD>
       artifact: docs/tickets/EPIC-NNNN-<slug>.md (and N child stories/tasks)
       approved_by: <user>
       notes: Approved ticket breakdown for EPIC-NNNN
     ```

5. **Recommend Next Step:**
   Inform the user that the approval is recorded, and recommend the next lifecycle command (e.g. *"Next: Run `/implement <task-id>` or `/pipeline` to see active tasks"*).

## Rules

- Never approve a document or ticket without explicit intent from the human.
- Always update both the frontmatter and `docs/decisions-log.md` in sync.
- Never fabricate approval dates; use the current session date.
