# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.12.0] — 2026-08-31

### Added
- Hook bus is now fired from the live ReAct loop (`on_start`, `on_iteration`, `before_llm`, `after_llm`, `before_tool`, `after_tool`, `on_final`)
- `Agent.last_trace` records tool calls and the final answer for the last run
- Memory exposed as first-class tools: `remember`, `recall`, `forget`
- Skill packs: JSON manifests under `.grok/skills/` (`agent.load_skills()`)
- Example `examples/skills_agent.py` + sample skill `examples/skills/workspace-greeter.json`
- Loop unit tests with a fake LLM (no live model)

### Changed
- Version bump to 0.12.0
- README / roadmap / HN drafts updated for the loop + skills release

## [0.11.0] — 2026-08-30

### Added
- File config: `grok-agent.toml` / `.grok/config.json` via `load_config()` and `grok-agent init`
- Event hooks (`HookBus`, `agent.on(...)`)
- MCP HTTP JSON-RPC client (`HTTPMCPClient`, `grok-agent mcp-http`)
- CLI `grok-agent tools`
- Examples: `hooks_agent.py`, `config_agent.py`
- `scripts/install.sh` one-liner
- Tests for config, hooks, HTTP client construction

### Changed
- `create_agent()` seeds defaults from discovered config + env
- Version bump to 0.11.0

## [0.10.0] — 2026-08-29

- MultiLLMRouter, memory CLI, orchestrator, `--router`

## [0.9.1] — 2026-08-28

- Named sessions, MCP resources/read, auto-register discovered MCP tools

## [0.9.0] — 2026-08-27

- Real MCP stdio JSON-RPC client and bundled echo server
