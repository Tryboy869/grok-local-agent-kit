# HN / Indie Hackers update — v0.31.0 (2026-09-18)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools, workspace RAG, multi-agent teams whose roster and blackboard survive restarts — and now a file-backed handoff queue so overnight jobs can claim work without a hosted broker.

## What's new this week
- v0.30: persist team roster (JSON / SQLite) + optional per-member `provider`/`model` bindings. `grok-agent roster demo`.
- v0.31: `HandoffQueue` — offer / claim / complete / drop. Mirrors onto the blackboard. `grok-agent handoff demo`.
- README feature list finally matches the shipped version.

## Indie Hackers angle
Most "multi-agent" demos die when the process exits. This kit writes the team, the board, and the work items to the workspace. Cron can resume. No Redis, no SaaS queue, no API key for the happy path.

## Ask
Would you rather we ship a 20s terminal GIF next, or a Test PyPI package?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
