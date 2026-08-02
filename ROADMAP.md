# Public Roadmap — grok-local-agent-kit

## ✅ v0.6.0 (current) — MVP public-ready

- Real Agent with ReAct-style tool loop + clearer iteration logging
- Multi-LLM: Ollama + OpenAI-compatible (LM Studio, vLLM…)
- Tools: web search, file read/write/list (cwd-safe by default), safe shell, execute_python, calculator
- Tool-result truncation + clearer connection errors
- Provider aliases (`lmstudio` handled in factory)
- Enhanced MCP stub (discovery + call placeholders, ready for real client)
- CLI (`grok-agent`) with `doctor` (LLM ping + tools list)
- Ready-to-run examples: chat, automation, research
- Unit tests aligned with current API (no live LLM required)
- Polished README, CONTRIBUTING, one-command install

## 🚧 v0.6.x / v0.7 — Real MCP

- Full MCP client (stdio + HTTP/SSE)
- Discover & call tools from external MCP servers
- Resource & prompt support
- Config file / env for MCP server list

## 📋 v0.8 — Multi-agent

- Agent-to-agent messaging
- Simple orchestrator / swarm patterns
- Shared tool registry

## 📋 v0.9 — Memory & persistence

- Conversation history to disk
- Vector memory (local embeddings)
- Session management

## 📋 v1.0 — Production ready

- Vision / multimodal models
- Skill marketplace format
- Sandboxed code execution (stronger isolation)
- Official docs site
- PyPI release with stable API

## Ideas / later

- Browser automation tool (Playwright)
- GUI (optional)
- Distributed agents over local network
- Evaluation harness

---

Want something prioritized? Open an issue or PR.
