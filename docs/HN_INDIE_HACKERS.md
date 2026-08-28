# Launch note — Grok Local Agent Kit v0.9.1

Suggested title:

**Show HN: Offline-first Python agents with real tool calling + MCP stdio (Ollama / LM Studio)**

---

Local models got good enough to *act*, not just chat. This kit is a small Python package that gives them a ReAct loop, 21 built-in tools, named sessions, and a working MCP stdio client.

## Why

Most “local agent” repos are wrappers around one vendor SDK, or they fake tool calling with regex. This one talks native Ollama tools *and* any OpenAI-compatible server (LM Studio, vLLM). File tools stay inside the cwd. Shell and `execute_python` are blocklisted. Tests do not need a live LLM.

v0.9.1 ships JSON-RPC MCP over stdio (`initialize`, `tools/list`, `tools/call`, `resources/list`, `resources/read`), auto-registers discovered MCP tools as `mcp_<server>_<tool>`, and stores named histories in `.grok/sessions/`.

## One-command try

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream --session demo
python examples/mcp_agent.py --no-llm
python examples/session_agent.py --session demo
```

## What’s in

- Multi-LLM routing (Ollama / LM Studio / OpenAI-compat)
- Tools: web, HTTP, files, hardened shell, sandbox Python, calculator, system info, live MCP
- Named sessions + CLI `/session` `/attach-mcp`
- MIT, Python 3.10+, CI on 3.10–3.12

## Not yet

- MCP HTTP/SSE transport
- Multi-agent orchestration / vector memory
- Token streaming *during* tool-call turns

Repo: https://github.com/Tryboy869/grok-local-agent-kit
Built autonomously by Grok · Nexus Studio / Tryboy869
