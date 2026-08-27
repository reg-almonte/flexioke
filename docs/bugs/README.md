# Bug Reports

Filed automatically by `/run-tests` (Phase 6) when test execution or a check
sheet turns up failures, named `<slug>.md` matching the feature's slug. One
consolidated report per feature — later runs append new failures to an
already-open report rather than creating duplicates.

Unlike every other artifact in `docs/`, bug reports do **not** use the
approval-frontmatter convention (`draft/pending-approval/approved/
superseded`). Filing one is an objective observation, not a decision, so it
needs no human sign-off. Instead they carry their own lifecycle:

```markdown
---
status: open | in-progress | fixed | wontfix
filed_at:
---
```

Phase 7 (`/bugfix`) reads `open`/`in-progress` reports, root-causes every
listed failure, and — once the human approves — applies fixes on a
`bugfix/<slug>` branch and opens/updates a PR. That's where the human
approval gate actually lives; bug-triager itself never flips the status to
`fixed`. Only Phase 6, by actually re-running clean, does that.

`/fix-until-green <story-or-epic-id>` loops Phase 6 and 7 automatically
(re-testing after each approved fix) until the report closes — with no
iteration cap, so it keeps going until clean or you interrupt it. Each
individual fix still needs your approval; the loop only automates the
re-test step in between. See [../../AI-DLC-Setup-Plan.md](../../AI-DLC-Setup-Plan.md).
