# Launch note — Grok Local Agent Kit v0.9.0

Suggested title:

**Show HN: Offline-first Python agents with real tool calling + MCP stdio (Ollama / LM Studio)**

---

Local models got good enough to *act*, not just chat. This kit is a small Python package that gives them a ReAct loop, 20 built-in tools, and a working MCP stdio client.

## Why

Most “local agent” repos are wrappers around one vendor SDK, or they fake tool calling with regex. This one talks native Ollama tools *and* any OpenAI-compatible server (LM Studio, vLLM). File tools stay inside the cwd. Shell and `execute_python` are blocklisted. Tests do not need a live LLM.

v0.9.0 ships a real JSON-RPC MCP client over stdio: `initialize`, `tools/list`, `tools/call`, `resources/list`. A bundled echo server lets you try MCP with `python examples/mcp_agent.py --no-llm`.

## One-command try

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
# have Ollama running with llama3.2, or LM Studio on :1234
grok-agent doctor
grok-agent chat -v --stream
```

MCP without an LLM:

```bash
python examples/mcp_agent.py --no-llm
```

## What’s in

- Multi-LLM routing (Ollama / LM Studio / OpenAI-compat)
- Tools: web search, HTTP GET, files (read/write/append/delete/search/mkdir/copy/stat), hardened shell, sandbox Python, calculator, system info
- MCP config via `GROK_MCP_SERVERS` or `.mcp_servers.json`
- CLI: `grok-agent chat` / `doctor`, `/save` `/load` `/tools` `/mcp` `/ping`
- MIT, Python 3.10+, CI on 3.10–3.12

## Not yet

- MCP HTTP/SSE transport
- Multi-agent orchestration / vector memory
- Token streaming *during* tool-call turns (final answers already stream)

Repo: https://github.com/Tryboy869/grok-local-agent-kit
Built autonomously by Grok · Nexus Studio / Tryboy869
