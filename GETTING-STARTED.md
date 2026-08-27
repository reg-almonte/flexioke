# Getting Started

A one-page cheat sheet for using this AI-DLC environment. For the full
rationale behind each phase, see [AI-DLC-Setup-Plan.md](AI-DLC-Setup-Plan.md).
The rules Gemini and Antigravity agents follow live in [GEMINI.md](GEMINI.md).

## 0. Create your project

Two ways to start a new project from this template:

- **GitHub:** click "Use this template" on this repo, then clone your new one.
- **Local copy:** from this repo, run
  `scripts/new-project.ps1 -Destination <path>` (Windows) or
  `scripts/new-project.sh <path>` (Mac/Linux/Git Bash) to copy the scaffold
  into a new folder and `git init` it.

If you're already reading this inside a generated project, this step is done.

## 1. Open it in Gemini / Antigravity

`cd` into the project and launch Antigravity (`agy` or Antigravity IDE) there. `GEMINI.md` is read
automatically — it's the operational ruleset every phase below follows.

> [!TIP]
> Run `/pipeline` at any time to see your current phase status and get the exact next command recommended for you!

## 2. Walk the phases, one command at a time

| # | Skill / Command | What happens | You do |
|---|---|---|---|
| — | `/pipeline` | Scans workspace & renders pipeline status board | Review next recommended action |
| — | `/approve <doc-or-epic>` | Updates frontmatter to `status: approved` and logs audit entry | Confirm approval |
| 1 | `/requirements <topic>` | Interview → requirements doc → functional spec | Approve both |
| 2 | `/design` | Proposes options → drafts an ADR | Pick an option, approve |
| 3 | `/tickets` | Breaks the ADR into Epic → Stories → Tasks | Approve the breakdown |
| 4 | `/implement <task>` | Writes code + opens PR (auto-reviewed, Phase 4.5) | Review the PR, merge yourself |
| 5 | `/write-tests <story>` | Writes tests + check sheet (auto-reviewed, Phase 5.5) | Approve the check sheet |
| 6 | `/run-tests <story>` | Runs tests/check sheet, files a bug report if needed | Nothing — it's automatic |
| 7 | `/bugfix <bug>` | Root-causes and proposes a fix as a PR | Approve the fix |
|   | `/fix-until-green <story>` | Loops 6 + 7 automatically until clean | Approve each fix, same as above |
| 8 | `/deploy-local` | Sets up and runs the project locally, automatically | Confirm it looks right |
| 9 | `/release <version>` | Packages a release manifest + deployment checklist | Approve it, then it's tagged |

## 3. Operational Speeds (Tiered Paths)

You don't have to run every phase for every change:
- **Full Path (Phases 1 → 9):** New features & major architecture decisions.
- **Fast-Track Bugfix (Phases 6 ↔ 7):** Fix bugs directly via `/bugfix` or `/fix-until-green`.
- **Direct Task / Chore (Phases 3 → 4.5):** Minor tasks or refactoring covered by existing ADRs.

## 4. The one rule to remember

**Nothing moves to the next phase until you approve the current one.**
Every doc carries a `status:` header (`draft` → `pending-approval` →
`approved`); the agent checks it before building on top. Use `/approve <path>` to approve single docs or batch tickets easily.

## 5. Where to go deeper

- [GEMINI.md](GEMINI.md) — the operational rules followed every phase
- [AI-DLC-Setup-Plan.md](AI-DLC-Setup-Plan.md) — full design rationale, traceability graph, roadmap
- `docs/decisions-log.md` — append-only audit trail of every approval
