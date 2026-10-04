# HN / Indie Hackers update — v0.44.0 (2026-10-04)

## One-liner
Local-first Python agent kit: a file-backed job ledger runs declarative workflows (files, injectable search, MCP echo) with no daemon, while chat and automation examples still route to Ollama or LM Studio when they are up.

## What's new
- v0.44: `grok-agent jobs demo` and `examples/jobs_agent.py`.
- Due jobs only. Second tick at the same clock is a no-op. State lands in `jobs-state.json`.
- Still: multi-LLM router, web search, workspace file tools, MCP attach, workflow runner, catalog-aware model pick.

## Indie Hackers angle
The first 10 minutes of a local-agent repo are "install Ollama, pull a model, hope tool calling works." Jobs and workflows are demonstrable before any of that. Live backends stay optional.

## Draft post
**Title:** Show HN: local agent kit — scheduled workflows, no model server

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent jobs demo
python examples/jobs_agent.py
python examples/chat_agent.py          # needs Ollama or LM Studio
python examples/automation_agent.py    # needs a local model
```

Ask: recorded GIFs next, or a Test PyPI release?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`

## Update — 2026-10-04 (v0.44)

### Hacker News (comment or follow-up Show HN)

Title: Show HN: Local agent kit – scheduled jobs without a daemon (v0.44)

v0.44 of grok-local-agent-kit adds a file-backed job ledger. A job is a JSON workflow (list files, write a note, injectable web search, MCP echo). `tick` runs only what is due. The clock is injectable, so CI never sleeps and never starts Ollama.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent jobs demo
python examples/jobs_agent.py
# when a local model is up:
python examples/chat_agent.py
python examples/automation_agent.py
```

Routing is unchanged: Ollama then LM Studio, circuit breaker on the hot path (`grok-agent route demo`). Not on PyPI yet. No recorded GIF in-tree (storyboard only).

Repo: https://github.com/Tryboy869/grok-local-agent-kit

### Indie Hackers

Shipped v0.44 today. The wedge is still local agents with no cloud key. New piece: a job ledger that runs the workflow runner on an interval and remembers the last tick in `jobs-state.json`. One curl install. Chat agent and automation agent examples stay ready when Ollama or LM Studio is running. Next honest milestone is still Test PyPI plus a 12s GIF. Not monetizing this.
