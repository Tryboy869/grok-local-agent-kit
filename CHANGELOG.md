# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.8.0] — 2026-08-16

### Added
- MCP foundation: load server list from `GROK_MCP_SERVERS` env or `.mcp_servers.json` / `.grok/mcp.json`
- Configurable `tool_result_max_chars` on `Agent`
- `CHANGELOG.md` and clearer package layout notes

### Improved
- System prompt guidance for file/code tools
- MCP tool responses now reflect configured servers (still stub until real stdio/SSE client)
- README / ROADMAP / version alignment for public MVP
- Package excludes empty `src/` leftovers

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series

## [0.7.5] — previous

- Real final-answer streaming (`stream=True` / CLI `--stream`)
- CLI env defaults + interactive helpers
- 12 tools, history save/load, multi-LLM (Ollama + LM Studio / OpenAI-compat)
- Ready-to-run examples and unit tests
