# HN / Indie Hackers update — v0.42.0 (2026-10-01)

## One-liner
Local-first Python agent kit: the real tool loop (list files, write a note) now runs with zero model servers via a scripted LLM, and the same Agent class still routes to Ollama or LM Studio when they are up.

## What's new
- v0.42: `grok-agent offline demo` and `examples/offline_chat_agent.py` / `examples/offline_automation_agent.py`.
- `Agent(llm=...)` so tests and CI never touch a daemon.
- Still: multi-LLM router, web search, workspace file tools, MCP attach, catalog-aware model pick.

## Indie Hackers angle
The first 10 minutes of a local-agent repo are "install Ollama, pull a model, hope tool calling works." This release makes the loop demonstrable before any of that. Live backends stay optional.

## Draft post
**Title:** Show HN: local agent kit — tool loop runs with no model server

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent offline demo
python examples/offline_chat_agent.py
python examples/offline_automation_agent.py
# when a daemon is up:
python examples/chat_agent.py
python examples/automation_agent.py
```

Ask: recorded GIFs next, or a Test PyPI release?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
