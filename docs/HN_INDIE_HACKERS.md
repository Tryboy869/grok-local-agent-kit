# HN / Indie Hackers update — v0.40.0 (2026-09-28)

## One-liner
Local-first Python agent kit: list the models actually sitting on your Ollama / LM Studio box and persist them to `catalog.json` — tests inject fake HTTP so CI never pings a daemon.

## What's new this week
- v0.36–0.38: circuit breaker on the router, persist to `health.json`.
- v0.39: portable kit snapshot.
- v0.40: `grok-agent models demo` writes `catalog.json` with reachable backends + model names.

## Indie Hackers angle
"Which model is installed?" is the first support question after "is Ollama running?". The catalog answers both without opening a chat session.

## Draft post
**Title:** Show HN: local-first agent kit — dump the models on your machine without chatting

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent models demo
python examples/catalog_agent.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Ask: Wire catalog.pick into the router next, or Test PyPI?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
