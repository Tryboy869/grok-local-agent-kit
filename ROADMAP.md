# Public Roadmap — grok-local-agent-kit

## ✅ v0.6.x — MVP foundation

- Real Agent with ReAct-style tool loop
- Multi-LLM: Ollama + OpenAI-compatible (LM Studio, vLLM…)
- Tools: web search, file ops (cwd-safe), safe shell, execute_python, calculator, get_datetime
- CLI (`grok-agent`) with doctor
- Ready-to-run examples + unit tests
- One-command install

## ✅ v0.7.0 (current)

- Conversation history persistence (`save_history` / `load_history`)
- New tool: `list_tools` (introspect available tools)
- 12 built-in tools
- Cleaner package (removed empty `src/` stubs)
- Polished README + contribution guide
- Ready for real MCP client integration

## 🚧 v0.7.x / v0.8 — Real MCP client

- Full MCP client (stdio + HTTP/SSE)
- Discover & call tools from external MCP servers
- Resource & prompt support
- Config file / env for MCP server list
- Optional `mcp` extra dependency

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
- Streaming responses

## Ideas / later

- Browser automation (Playwright)
- Optional GUI
- Distributed agents over local network
- Evaluation harness
- Windows/macOS packaging notes

---

Want something prioritized? Open an issue or PR.
