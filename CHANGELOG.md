# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.14.0] — 2026-09-02

### Added
- Optional Ollama embeddings (`GROK_EMBED_BACKEND=ollama`, `GROK_EMBED_MODEL`) with hash fallback
- `on_thought` hook + thought entries in `Agent.last_trace` during the ReAct loop
- Stronger `execute_python` sandbox: more blocked imports/calls, dunder guard, wall-clock timeout
- `examples/embed_agent.py` and `examples/sandbox_agent.py` (no live LLM required)
- Demo storyboard under `docs/gifs/README.md`

### Changed
- Vector memory uses the shared `embeddings` module (stable MD5-hashed bag-of-words)
- Usage tracker records thought tokens via `on_thought`
- README / roadmap / HN drafts updated for v0.14.0

## [0.13.0] — 2026-09-01

### Added
- SQLite bag-of-words vector memory (`vremember` / `vrecall` / `vforget`) — no extra deps
- Tools `vremember` and `vrecall` registered on the default agent
- MCP Streamable HTTP / SSE client with exponential backoff (`SSEMCPClient`, `grok-agent mcp-sse`)
- MCP prompts: `prompts/list` and `prompts/get` on stdio client + manager
- Usage tracker (`UsageStats`, `agent.usage.summary()`)
- `on_token` hook fired when the final answer is produced / streamed
- Example `examples/vector_memory_agent.py` (no live LLM)
- Tests for vector ranking, usage, and SSE parsing

### Changed
- Version bump to 0.13.0
- README / roadmap / HN drafts updated for vector memory + SSE + prompts

## [0.12.0] — 2026-08-31

### Added
- Hook bus is now fired from the live ReAct loop
- `Agent.last_trace` records tool calls and the final answer for the last run
- Memory exposed as first-class tools: `remember`, `recall`, `forget`
- Skill packs under `.grok/skills/`
- Loop unit tests with a fake LLM (no live model)

## [0.11.0] — 2026-08-30

- File config, hooks, MCP HTTP, CLI tools, install.sh

## [0.10.0] — 2026-08-29

- MultiLLMRouter, memory CLI, orchestrator, `--router`

## [0.9.1] — 2026-08-28

- Named sessions, MCP resources/read, auto-register discovered MCP tools

## [0.9.0] — 2026-08-27

- Real MCP stdio JSON-RPC client and bundled echo server
