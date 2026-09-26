# HN / Indie Hackers update — v0.38.0 (2026-09-26)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router that **writes circuit-breaker decisions to health.json**, so the next process skips a dead backend without pinging it again.

## What's new this week
- v0.36: standalone health board (`health demo|show|trip|reset`).
- v0.37: that board is on the hot path. `pick` / `probe` / `chat` skip open breakers.
- v0.38: those decisions persist. `MultiLLMRouter.attach_persist("health.json")` hydrates a new process. `grok-agent route persist` proves it with fake clients.

## Indie Hackers angle
A crashed LM Studio used to burn every request in a new Python process. Now the first process trips the breaker and dumps `health.json`. The next CLI invocation never pings it. Same file the `health` CLI already uses.

## Draft post
**Title:** Show HN: local-first agent kit — router health now survives process restart

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent health demo
grok-agent route demo
grok-agent route persist
python examples/persist_route_agent.py
```

Ask: Test PyPI next, or a 20s GIF of `route persist`?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
