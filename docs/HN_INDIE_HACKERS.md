# HN / Indie Hackers update — v0.37.0 (2026-09-25)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router that now **refuses traffic to a tripped circuit breaker**, ReAct tools, workspace RAG, multi-agent teams, scriptable approval TUI, opt-in live eval.

## What's new this week
- v0.36: standalone health board (`health demo|show|trip|reset`).
- v0.37: that board is on the hot path. `MultiLLMRouter.pick` / `probe` / `chat` skip open breakers. `grok-agent route demo` proves it with fake clients — no GPU, no daemon.

## Indie Hackers angle
A dead LM Studio used to sit first in the chain and eat every request. Now two refused connections open the breaker; the next `pick()` never pings it. Same JSON file you can ship in a product.

## Draft post
**Title:** Show HN: local-first agent kit — circuit breaker actually sits on the LLM router

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent health demo
grok-agent route demo
python examples/route_health_agent.py
```

Ask: Test PyPI next, or a 20s GIF of `route demo`?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
