# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.8.7] — 2026-08-26

### Added
- `search_files` tool — cwd-safe text search in file contents (glob + query, with short snippets). **17 built-in tools**

### Improved
- Agent system prompt: guidance for `search_files` (find code / notes before reading)
- Version alignment (package, history format, User-Agent, docs)
- README demos, tool table, HN / Indie Hackers pitch
- Unit tests cover `search_files` and 17-tool registry
- Examples (chat / automation) mention the new tool

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series

## [0.8.6] — 2026-08-25

### Improved
- Agent system prompt: clearer routing guidance (list before write, prefer calculator / execute_python, careful shell)
- `run_shell` safety: expanded blocklist (rm -r, curl|sh, wget|sh, chmod 777, etc.)
- Version alignment (package, history format, User-Agent, docs)
- README demos, HN / Indie Hackers pitch, and example banners
- CONTRIBUTING + ROADMAP touch-ups for public MVP

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series
- 16 built-in tools unchanged; foundation for external MCP tools is ready for the real client

## [0.8.5] — 2026-08-24

### Added
- `delete_file` tool — cwd-safe single-file deletion (refuses directories); **16 built-in tools**

### Improved
- Agent loop: avoid redundant second LLM call when `stream=True` and final content is already available
- System prompt guidance for `delete_file`
- MCP foundation status strings slightly clearer
- README demos, tool table, HN / Indie Hackers share block
- Unit tests cover `delete_file` and 16-tool registry
- Version alignment across package, history format, docs

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series

## [0.8.4] — 2026-08-22

### Added
- `get_system_info` tool — OS, Python version, cwd, CPU count (15 built-in tools total)
- `examples/custom_tools_agent.py` — ready-to-run demo of `register_tools()` with domain tools

### Improved
- MCP foundation: clearer config error messages, safer server entry handling
- System prompt guidance for `get_system_info`
- Examples (chat / automation) updated for the new tool
- Unit tests cover `get_system_info` and 15-tool registry
- README + ROADMAP + version alignment

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series

## [0.8.3] — 2026-08-20

### Added
- `http_get` tool — simple HTTP GET with timeout and truncation (14 built-in tools total)
- `Agent.list_registered_tools()` helper

### Improved
- System prompt guidance for `http_get` vs `web_search`
- README: clearer demos, tool table, HN / Indie Hackers share section
- Examples banners and tool lists
- Unit tests cover the new tool and helper

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series

## [0.8.2] — 2026-08-19

### Added
- `append_file` tool (cwd-safe) — 13 built-in tools total
- `py.typed` marker for typing consumers

### Improved
- README: sharper demos, one-command install, HN / Indie Hackers share blurb
- Version alignment across package, history format, docs
- Slightly clearer automation / research example banners

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series

## [0.8.1] — 2026-08-18

### Improved
- Agent loop: clearer multi-tool iteration logging, safer argument parsing, versioned history files
- LLM client: more resilient error messages for Ollama / OpenAI-compatible backends
- MCP foundation: richer config loading feedback and clearer stub responses when servers are listed
- README: tighter quick-start, better demo descriptions (GIF-ready), HN/Indie Hackers friendly pitch
- Examples: slightly clearer goals and version banners
- Tests: keep zero live-LLM requirement

### Notes
- Full MCP client (stdio + HTTP/SSE) remains the primary focus of the 0.8.x series

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
