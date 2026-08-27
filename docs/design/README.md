# Design (ADRs)

One ADR per design decision, created by `/design` (Phase 2), named
`ADR-NNNN-<slug>.md` (4-digit sequential number, e.g. `ADR-0001-...`). Each
ADR reads an `approved` functional spec (`docs/specs/`) and must carry a
YAML frontmatter status header:

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by:
approved_at:
---
```

An ADR should present options and trade-offs; the human picks (or asks for
revisions) before it moves to `approved`. See
[../decisions-log.md](../decisions-log.md) and
[../../AI-DLC-Setup-Plan.md](../../AI-DLC-Setup-Plan.md).
