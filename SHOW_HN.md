# Show HN draft (copy-paste ready)

**Title (max ~80 chars):**

Show HN: Offline-first local agents with real tools, Ollama, and live MCP

**Body:**

I built an open-source Python toolkit for local AI agents that actually call tools — no cloud API key required if you run Ollama or LM Studio.

Why I made it: most "local agent" demos are chat wrappers. I wanted a small, installable kit with a ReAct loop, cwd-safe file tools, a restricted shell, web/http, Python exec, and a real MCP stdio client (initialize, tools/list, tools/call, resources/list).

What it does today (v0.9.0):

- Multi-LLM: Ollama native + any OpenAI-compatible endpoint (LM Studio)
- Real tool-calling loop + streaming of the final answer
- 20 built-in tools: web search, http_get, files (list/read/write/append/delete/search/mkdir/copy/stat), restricted shell, execute_python, calculator, datetime, system info, list_tools, live MCP
- Bundled echo MCP server for tests and demos
- CLI: `grok-agent chat` / `grok-agent doctor` with /save /load /reset /tools /mcp /ping
- Python API: `create_agent(...)`, history save/load, env defaults (`GROK_AGENT_*`, `GROK_MCP_SERVERS`)
- Unit tests that do not need a live LLM

Quick start:

```
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
ollama pull llama3.2
grok-agent doctor
grok-agent chat -v --stream
python examples/mcp_agent.py --no-llm
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Not affiliated with xAI. Built autonomously by Grok for Nexus Studio / Tryboy869. MIT.

Happy to hear what would make this useful for your local workflow (MCP HTTP/SSE and multi-agent memory are next).
