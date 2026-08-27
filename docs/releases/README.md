# Releases

Release manifests created by `/release` (Phase 9), named `<version>.md`
(e.g. `v1.0.0.md`). Each packages what a human needs to actually carry out a
production deployment: source reference, links to specs/design/tickets,
test evidence, known open issues, setup instructions, and a suggested
pre-deployment checklist. Carries the same YAML frontmatter status header:

```markdown
---
status: draft | pending-approval | approved | superseded
approved_by:
approved_at:
---
```

This tool never deploys anything to production itself or contacts real
infrastructure — `release-manager` packages and informs; a human (or their
separate ops process) deploys. A git tag for the release is only created
after this file is `approved`. See
[../decisions-log.md](../decisions-log.md) and
[../../AI-DLC-Setup-Plan.md](../../AI-DLC-Setup-Plan.md).
