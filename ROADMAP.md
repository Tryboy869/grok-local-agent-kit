# Public Roadmap — grok-local-agent-kit

## ✅ v0.6.x — MVP foundation

- Real Agent with ReAct-style tool loop
- Multi-LLM: Ollama + OpenAI-compatible (LM Studio, vLLM…)
- Tools: web search, file ops (cwd-safe), safe shell, execute_python, calculator, get_datetime
- CLI (`grok-agent`) with doctor
- Ready-to-run examples + unit tests
- One-command install

## ✅ v0.7.x

- Conversation history persistence (`save_history` / `load_history`)
- `list_tools`, 12+ built-in tools, CLI interactive helpers
- Env var defaults, `register_tools()`, streaming final answers
- Polished README + contribution guide

## ✅ v0.8.0 – 0.8.6 (current)

- MCP foundation: config via `GROK_MCP_SERVERS` / `.mcp_servers.json`
- Configurable tool-result truncation
- `append_file`, `http_get`, `get_system_info`, `delete_file`, `py.typed`
- Robustness pass on agent loop (smarter streaming, history versioning, routing guidance)
- Stronger shell safety blocklist
- 16 built-in tools + custom-tools example

## 🚧 v0.8.x — Real MCP client

- Full MCP client (stdio + HTTP/SSE)
- Discover & call tools from external MCP servers
- Resource & prompt support
- Optional `mcp` extra dependency
- Wire configured servers into the live tool registry

## 📋 v0.9 — Multi-agent & memory

- Agent-to-agent messaging
- Simple orchestrator / swarm patterns
- Shared tool registry
- Vector memory (local embeddings)
- Session management beyond basic JSON history

## 📋 v1.0 — Production ready

- Vision / multimodal models
- Skill marketplace format
- Stronger sandboxed code execution
- Official docs site
- PyPI release with stable API
- Full streaming throughout the tool loop

## Ideas / later

- Browser automation (Playwright)
- Optional GUI
- Distributed agents over local network
- Evaluation harness
- Windows/macOS packaging notes

---

Want something prioritized? Open an issue or PR.
