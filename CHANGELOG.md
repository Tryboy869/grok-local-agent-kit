# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.9.1] — 2026-08-28

### Added
- Named sessions under `.grok/sessions/` (`save_named_session`, `load_named_session`, CLI `--session`, `/session`, `/sessions`)
- MCP `resources/read` on the stdio client + `mcp_read_resource` tool (21 built-in tools)
- Auto-register discovered MCP tools as `mcp_<server>_<tool>` (`Agent.attach_mcp_tools()`, CLI `--attach-mcp` / `/attach-mcp`)
- Bundled echo server now serves `echo://about`
- `examples/session_agent.py`

### Changed
- Version bump to 0.9.1 across package metadata and MCP clientInfo

## [0.9.0] — 2026-08-27

### Added
- Real MCP **stdio JSON-RPC client** (`StdioMCPClient`, `MCPManager`)
- Bundled echo MCP server
- File tools: `mkdir`, `copy_file`, `file_stat`
- CLI helpers `/mcp` and `/ping`
- Launch draft: `docs/HN_INDIE_HACKERS.md`

## [0.8.7] — 2026-08-26

See git history for 0.8.x notes.
