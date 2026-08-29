# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.10.0] — 2026-08-29

### Added
- `MultiLLMRouter`: ordered fallback across Ollama and LM Studio / OpenAI-compat
- CLI `grok-agent route` probes every endpoint in the chain
- CLI `grok-agent memory {remember,recall,forget,stats}`
- Local JSONL memory (`.grok/memory/notes.jsonl`) + tools remember / recall / forget
- `Orchestrator` with planner + researcher / coder / operator roles
- Examples: `memory_agent.py`, `orchestrator_agent.py`
- Agent flag `use_router=` / env `GROK_AGENT_ROUTER=1` / CLI `--router`

### Changed
- Version bump to 0.10.0

## [0.9.1] — 2026-08-28

- Named sessions, MCP resources/read, auto-register discovered MCP tools

## [0.9.0] — 2026-08-27

- Real MCP stdio JSON-RPC client and bundled echo server
