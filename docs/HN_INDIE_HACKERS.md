# HN / Indie Hackers update — v0.39.0 (2026-09-27)

## One-liner
Local-first Python agent kit: one command dumps a portable snapshot of version, tools, and whether health/roster/board files exist — no model required.

## What's new this week
- v0.36–0.38: circuit breaker on the router, then persist those decisions to `health.json`.
- v0.39: `grok-agent snapshot demo` writes `kit-snapshot.json`. Same facts a maintainer would paste into an issue.

## Indie Hackers angle
Support threads stall on "what version / which tools / is health.json even there?". Snapshot is a one-file answer you can attach without starting Ollama.

## Draft post
**Title:** Show HN: local-first agent kit — dump a portable snapshot without a model

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent snapshot demo
python examples/snapshot_agent.py
```

Ask: Test PyPI next, or a 20s GIF of snapshot + route persist?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
