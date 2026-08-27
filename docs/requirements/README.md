# Requirements

One markdown file per feature/requirement, created by `/requirements <topic>`
(Phase 1). Each file must carry a YAML frontmatter status header:

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by:
approved_at:
---
```

Nothing in `docs/design/` may reference a requirements doc that isn't
`approved`. See [../decisions-log.md](../decisions-log.md) for the approval trail
and [../../AI-DLC-Setup-Plan.md](../../AI-DLC-Setup-Plan.md) for the full process.
