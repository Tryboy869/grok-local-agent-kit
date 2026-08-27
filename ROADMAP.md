# Public Roadmap — grok-local-agent-kit

## ✅ v0.6.x — MVP foundation

- Real Agent with ReAct-style tool loop
- Multi-LLM: Ollama + OpenAI-compatible (LM Studio, vLLM…)
- Tools: web search, file ops (cwd-safe), safe shell, execute_python, calculator, get_datetime
- CLI (`grok-agent`) with doctor
- Ready-to-run examples + unit tests
- One-command install

## ✅ v0.7.x

- Conversation history persistence
- Env var defaults, `register_tools()`, streaming final answers
- Polished README + contribution guide

## ✅ v0.8.x

- MCP *foundation* (config + stub tools)
- `append_file`, `http_get`, `get_system_info`, `delete_file`, `search_files`
- 17 tools, stronger shell blocklist

## ✅ v0.9.0 (current)

- **Real MCP stdio JSON-RPC client** (`StdioMCPClient` + `MCPManager`)
- Bundled echo MCP server + `examples/mcp_agent.py`
- File tools: `mkdir`, `copy_file`, `file_stat` (20 tools)
- CLI `/mcp` and `/ping`
- Public launch note for HN / Indie Hackers

## 🚧 v0.9.x

- MCP HTTP/SSE transport
- Auto-register discovered MCP tools into the live tool registry
- Prompts + resource reads (`resources/read`)
- Session directory + named histories

## 📋 v1.0 — Production ready

- Agent-to-agent / simple orchestrator
- Local vector memory
- Vision / multimodal models
- Stronger sandboxed code execution
- PyPI release with stable API
- Streaming throughout the tool loop
- Official docs site

## Ideas / later

- Browser automation (Playwright)
- Optional GUI
- Evaluation harness
- Windows/macOS packaging notes

---

Want something prioritized? Open an issue or PR.
