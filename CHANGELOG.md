# Changelog

All notable changes to grok-local-agent-kit are documented here.

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
