# Tickets

Epic > Story > Task tickets decomposed from an `approved` ADR, created by
`/tickets` (Phase 3). Each level gets its own file, named `EPIC-NNNN-<slug>.md`,
`STORY-NNNN-<slug>.md`, and `TASK-NNNN-<slug>.md` respectively (each type
numbered independently, 4 digits). Every file links back to its parent
(story → epic, task → story; the epic links to its ADR) and carries a YAML
frontmatter status header:

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by: user
approved_at: 2026-08-27
---
```

Story and Task files also carry an `implementation:` field (`pending` /
`in-progress` / `in-review`), owned by Phase 4 (the implementer) — set once
by `/tickets` to `pending` and updated only by `/implement` from then on.

Only `approved` tickets (i.e. "ready for implementation") may be picked up by
`/implement`. See [../decisions-log.md](../decisions-log.md) and
[../../AI-DLC-Setup-Plan.md](../../AI-DLC-Setup-Plan.md).
