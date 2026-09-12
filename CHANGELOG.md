# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.25.0] — 2026-09-12

### Added
- Plugin sandbox: Python `.py` plugins are **not imported** unless opted in
- Env: `GROK_AGENT_ALLOW_PY_PLUGINS=1` or `GROK_AGENT_PY_PLUGIN_ALLOWLIST=stem1,stem2`
- `discover_plugins(allow_py=...)` / `apply_plugins(..., allow_py=...)`
- `py_plugins_allowed()`, `skipped_py_plugins()`
- CLI: `grok-agent sandbox status|skipped`
- Example: `examples/sandbox_plugin_agent.py`
- Tests: `tests/test_v025.py` (no live LLM)

### Security
- JSON plugins remain data-only and load by default
- Untrusted workspace `.py` files no longer execute on `get_default_tools()` / `plugins list`

## [0.24.0] — 2026-09-11

### Added
- Drop-in tool plugins (`plugins.py`) from `./tools`, `~/.grok-agent/tools`, or `GROK_AGENT_PLUGIN_DIR`
- JSON plugins (`kind=template|json`) and Python plugins (`handler` / `register`)
- JSONL transcripts (`transcripts.py`, `grok-agent transcripts`)
- CLI: `grok-agent plugins list|dirs`
- Examples: `plugin_agent.py`, `transcript_agent.py`, `examples/tools/workspace_ping.json`
- Tests in `tests/test_v024.py` (no live LLM)

## [0.23.0] — 2026-09-11

### Added
- Optional sqlite-vec backend with hash cosine fallback
- `grok-agent vec info|search|remember`
