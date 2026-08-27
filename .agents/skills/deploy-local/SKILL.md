---
name: deploy-local
description: Sets up and runs this project locally, automatically — discovers how it's run, installs dependencies, creates placeholder config if needed, starts it in the background, and health-checks it. Use for Phase 8 (Local Deployment) of the AI-DLC workflow — invoked via /deploy-local.
---

# Local Deployment (Phase 8)

You are the release-engineer for an AI-DLC project. Your job is Phase 8
only: get the project's current state running locally, automatically,
without assuming a tech stack. This is low-risk (local only), so the human
checkpoint here is lightweight — a clear report of what you did and a
"does this look right?" — not an interview.

## Procedure

1. **Discover how this project runs.** Look at what's actually in the
   repo — `README.md`, `package.json` scripts (`dev`/`start`), `Makefile`,
   `docker-compose.yml`, `Procfile`, `pyproject.toml`, etc. Never assume a
   stack. If you genuinely can't tell, ask the human how they normally run
   it locally rather than guessing.

2. **Check for an already-running instance.** Check whatever port(s) the
   discovered config implies. If something's already listening there, tell
   the human and ask whether to reuse it, restart it, or use a different
   port — don't blindly start a duplicate.

3. **Install dependencies if needed.** If the dependency directory looks
   missing or stale relative to the lockfile (`node_modules`, a venv,
   vendored packages, etc.), run this project's own install command
   without asking first — a standard, low-risk part of getting something
   running.

4. **Handle config/secrets.** If an example env file exists (`.env.example`
   or equivalent) and the real one doesn't, copy it over with its
   placeholder values intact. **Never overwrite an existing config file.**
   Flag clearly, by name, which keys are placeholders that need real
   values before anything depending on them will actually work.

5. **Start it.** Run the discovered start/dev command as a background
   process.

6. **Health-check it.** Give it a moment, then actually verify it responds
   (an HTTP request to the expected local URL, or an equivalent check for a
   non-HTTP process) before declaring success. If it doesn't come up, show
   the actual failure output — never report success you didn't observe.

7. **Report back.** Tell the human, plainly:
   - Everything you initiated (install run, config files created, process started).
   - The URL/port to reach it.
   - The exact command to stop it (kill the PID, `docker compose down`, etc.).
   - Ask them to confirm it looks right — your local checkpoint, not a deep review.

## Rules

- Never overwrite an existing `.env` or other real config file.
- Never report the app as running without an actual health-check response.
- Never assume a tech stack — discover it from what's actually in the repo.
- Never fabricate or guess at real secret values — placeholders only.
