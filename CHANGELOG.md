# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.9.0] — 2026-08-27

### Added
- Real MCP **stdio JSON-RPC client** (`StdioMCPClient`, `MCPManager`)
- Bundled echo MCP server (`python -m grok_local_agent_kit.mcp_echo_server`)
- `examples/mcp_agent.py` (works with `--no-llm`)
- File tools: `mkdir`, `copy_file`, `file_stat` — **20 built-in tools**
- CLI helpers `/mcp` and `/ping`
- Launch draft: `docs/HN_INDIE_HACKERS.md`

### Changed
- `mcp_list_*` / `mcp_call_tool` now talk to live stdio servers instead of stubs
- Version bump across package, history format, User-Agent, docs

### Notes
- HTTP/SSE MCP transport is still pending (0.9.x)

## [0.8.7] — 2026-08-26

See git history for 0.8.x notes. Focus of 0.8.x was MCP foundation, search_files, and robustness.
