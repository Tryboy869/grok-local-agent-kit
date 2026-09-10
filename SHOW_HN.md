# Show HN: grok-local-agent-kit — offline-first local agents (Ollama + MCP)

Title (HN):
Show HN: A small Python kit for local agents with Ollama, MCP, and a tool cache

---

Paste-ready body:

I built a small Python toolkit for agents that stay on your machine.

Problem: most agent frameworks assume a cloud LLM + embeddings API. I wanted something that boots against Ollama or LM Studio, calls real tools, speaks MCP, and does not phone home.

grok-local-agent-kit (v0.21):

- ReAct tool loop (files, shell, python sandbox, calculator, custom tools)
- Ollama + LM Studio / OpenAI-compat with a fallback router
- MCP over stdio, Streamable HTTP (session ids), and SSE + JSON-RPC cancel
- TTL cache so identical tool calls are free
- Offline telemetry (latency, hits, errors) — no network
- Local HTTP API, eval harness, recipes, watcher

Install:

    curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
    grok-agent doctor
    python examples/cache_agent.py

Or:

    pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Happy to hear what is missing for your local-agent workflow.
