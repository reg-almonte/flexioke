# Functional Specs

The final output of Phase 1, created by `/requirements` (Stage B, after the
requirements doc is approved), named `<slug>.md` matching its requirements
doc's slug. Captures precise functional behavior — flows, inputs/outputs,
business rules, data entities — as opposed to the requirements doc's
why/who/goals. Carries the same YAML frontmatter status header:

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by:
approved_at:
---
```

Phase 2 (`/design`) gates on this file being `approved`, not the
requirements doc directly. See [../decisions-log.md](../decisions-log.md)
and [../../AI-DLC-Setup-Plan.md](../../AI-DLC-Setup-Plan.md).
