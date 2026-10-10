## [0.49.0] - 2026-10-10

### Added
- Ready-to-run core MVP demo: `examples/mvp_core_demo.py` showcases offline intent routing, file/math/system/MCP tools, and multi-LLM provider probes in one script.
- Confirms the agent loop works with zero models installed; live chat/automation examples remain available once Ollama or LM Studio is up.
- Docs note in README for the new one-command demo path.

### Changed
- Version bump for the polished offline MVP entry point.


## [0.48.0] - 2026-10-09

### Added
- Session pack (`run_pack`, `load_pack`, `demo_pack`) batches chat, file automation, search, and MCP echo through the offline MVP router.
- Writes `SESSION.md` and `pack-report.json`. Provider probe is opt-in and never fails the demo.
- CLI: `grok-agent pack demo` and `grok-agent pack run --file PATH`.
- Examples: `examples/session_pack.py`, `examples/packs/local_session.json`.
- Tests: `tests/test_v048.py` (no network).
- GIF storyboard `docs/gifs/pack-demo.md`.
- HN / Indie Hackers draft `docs/HN_UPDATE_v048.md`.

## [0.47.0] - 2026-10-08

### Added
- `execute_handoff` calls the ReAct loop when the playbook handoff mode is `react`.
- Injected callable for tests and `scripted_react` for an offline demo. `live=True` calls `Agent.run` (Ollama or LM Studio) and records failures instead of raising.
- CLI: `grok-agent handoff demo` and `grok-agent handoff live`.
- Example: `examples/handoff_react_agent.py`.
- Tests: `tests/test_v047.py` (no network).
- GIF storyboard `docs/gifs/handoff-demo.md`.
- HN / Indie Hackers draft `docs/HN_UPDATE_v047.md`.

## [0.46.0] - 2026-10-07

### Added
- Playbook runner (`run_playbook`, `load_playbook`) sequences the offline MVP: files, math, system, search, MCP echo.
- Handoff descriptor: `mode=react` when Ollama or LM Studio probe is up; `mode=scripted` otherwise. No chat socket is opened.
- CLI: `grok-agent playbook demo` and `grok-agent playbook run PATH`.
- Examples: `examples/playbook_agent.py`, `examples/playbooks/local_mvp.json`.
- Tests: `tests/test_v046.py` (injected probes, no network).
- GIF storyboard `docs/gifs/playbook-demo.md`.
- HN / Indie Hackers draft `docs/HN_UPDATE_v046.md`.

## [0.45.0] - 2026-10-06

### Added
- Offline MVP runner: intent routing (files, math, search, system, MCP echo) plus the shared tool registry.
- Multi-LLM provider table for Ollama (`:11434`) and LM Studio (`:1234/v1`) with a non-fatal probe.
- `grok-agent mvp`, `examples/mvp_chat.py`, `examples/mvp_automation.py`.
- GIF storyboard `docs/gifs/mvp-demo.md`.

# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.43.0] — 2026-10-02

### Added
- Declarative workflow runner (`Workflow`, `run_workflow`, `load_workflow`) — file ops, injectable web search, MCP echo
- Offline demo chains a chat-style list, an automation write, a search fixture, and an MCP call (no daemon)
- CLI: `grok-agent workflow demo` and `grok-agent workflow run PATH`
- Example: `examples/workflow_agent.py` and `examples/workflows/mvp.json`
- Tests: `tests/test_v043.py` (cwd-safe paths, no network)
- GIF storyboard in `docs/gifs/workflow-demo.md` (binary capture still optional)
- HN / Indie Hackers update draft in `docs/HN_INDIE_HACKERS.md`
