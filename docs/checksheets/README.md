# Check Sheets

QA verification checklists created by `/write-tests` (Phase 5), named
`<slug>.md` matching the feature's slug. Each item maps a functional-spec/
design point to a verification check (automated test or manual step),
checked off only once its backing test has actually been run and passed.
Carries the same YAML frontmatter status header:

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by:
approved_at:
---
```

After drafting, `/write-tests` automatically triggers Phase 5.5 (the
`checksheet-reviewer`), which appends a `## Completeness Review` section
checking the sheet against the functional spec/ADR/tickets — advisory only,
never a merge/approval gate itself. Re-run it standalone with
`/review-checksheet`. See [../decisions-log.md](../decisions-log.md) and
[../../AI-DLC-Setup-Plan.md](../../AI-DLC-Setup-Plan.md).
