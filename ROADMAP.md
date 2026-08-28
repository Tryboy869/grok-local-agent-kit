# Public Roadmap — grok-local-agent-kit

## ✅ v0.6.x — MVP foundation

- Real Agent with ReAct-style tool loop
- Multi-LLM: Ollama + OpenAI-compatible (LM Studio, vLLM…)
- Tools, CLI, examples, tests, one-command install

## ✅ v0.7.x

- Conversation history persistence, streaming final answers

## ✅ v0.8.x

- MCP foundation + extra file/http tools

## ✅ v0.9.0

- Real MCP stdio JSON-RPC client + echo server + 20 tools

## ✅ v0.9.1 (current)

- Named session directory (`.grok/sessions/`)
- MCP `resources/read` + `mcp_read_resource`
- Auto-register discovered MCP tools into the live registry

## 🚧 v0.9.x

- MCP HTTP/SSE transport
- MCP prompts
- Token streaming throughout the tool loop

## 📋 v1.0 — Production ready

- Agent-to-agent orchestrator
- Local vector memory
- Vision / multimodal models
- Stronger sandboxed code execution
- PyPI release with stable API
- Official docs site

Want something prioritized? Open an issue or PR.
