# HN / Indie Hackers update — v0.36.0 (2026-09-24)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools, workspace RAG, multi-agent teams, scriptable approval TUI, opt-in live eval, and a circuit breaker so a dead local backend stops eating requests.

## What's new this week
- v0.35: `grok-agent eval-demo` / `eval-live`. Stub in CI; real models need `--live` **and** `GROK_LIVE_EVAL=1`.
- v0.36: `grok-agent health demo|show|trip|reset`. Closed / open / half-open per backend. JSON on disk. Zero LLM.

## Indie Hackers angle
Local models flap. The kit now records those flaps without a GPU: two refused connections open the LM Studio breaker, cooldown moves it half-open, a later success closes it. Same file you can tail in a product.

## Draft post
**Title:** Show HN: local-first agent kit + circuit breaker for Ollama / LM Studio

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent health demo
grok-agent eval-demo
python examples/health_agent.py --demo
```

Ask: Wire the breaker into MultiLLMRouter next, or Test PyPI?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
