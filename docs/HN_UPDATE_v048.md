# HN / Indie Hackers update — v0.48.0 (2026-10-09)

Title: Show HN: grok-local-agent-kit — offline session pack for local agents (Ollama / LM Studio)

## Post

I keep building a local-first Python kit for agents. v0.48 adds a session pack: one command runs a chat goal, a file automation, a search fixture, and an MCP echo, then writes `SESSION.md` plus `pack-report.json`. No cloud key. No model required for the demo.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent pack demo
python examples/session_pack.py
```

What is already in the box:

- Multi-LLM table for Ollama (`:11434`) and LM Studio (`:1234/v1`), circuit breaker, optional probe
- ReAct tool loop, file tools, web search with HTML fallback, MCP stdio/HTTP/SSE
- Playbook runner and opt-in ReAct handoff (`grok-agent handoff demo`)
- Team, blackboard, roster, approval gate

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT. Python >= 3.10.

Honest status: 1 star, 0 forks, not on PyPI yet. The pack demo does not call a model. `--probe` only checks whether a local daemon answers.

## Indie Hackers blurb

Shipped v0.48 of grok-local-agent-kit: a one-command session pack that routes chat, file automation, search, and MCP echo offline, then writes a markdown brief. Still pre-PyPI. Looking for people who already run Ollama and want a small, testable agent toolkit rather than another hosted wrapper.
