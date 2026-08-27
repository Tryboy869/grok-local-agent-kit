# Show HN draft (copy-paste ready)

**Title (max ~80 chars):**

Show HN: Grok Local Agent Kit – offline-first agents with real tools, Ollama/MCP

**Body:**

I built an open-source Python toolkit for local AI agents that actually call tools — no cloud API key required if you run Ollama or LM Studio.

Why I made it: most "local agent" demos are chat wrappers. I wanted a small, installable kit with a ReAct loop, cwd-safe file tools, a hardened shell, web/http, Python exec, and an MCP foundation you can grow into a full client.

What it does today (v0.8.7):

- Multi-LLM: Ollama native + any OpenAI-compatible endpoint (LM Studio)
- Real tool-calling loop + streaming of the final answer
- 17 built-in tools: web search, http_get, files (list/read/write/append/delete/search), hardened shell, execute_python, calculator, datetime, system info, list_tools, MCP stubs
- CLI: `grok-agent chat` / `grok-agent doctor` with /save /load /reset /tools
- Python API: `create_agent(...)`, `register_tools()`, history save/load
- Unit tests that do not need a live LLM

Quick start:

```
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
ollama pull llama3.2
grok-agent doctor
grok-agent chat -v --stream
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Not affiliated with xAI. Built autonomously by Grok for Nexus Studio / Tryboy869. MIT.

Happy to hear what would make this useful for your local workflow (full MCP client is next).
