## [0.52.0] - 2026-10-14

### Added
- Smarter offline intent routing in the core MVP: better math expression detection (regex + more keywords) and expanded phrases for files, system, search, and MCP.
- Ready-to-run examples remain the primary onboarding path; core loop is more reliable without any model.
- Docs: `docs/HN_UPDATE_v052.md` prepared for Hacker News / Indie Hackers.

### Changed
- Version bump to 0.52.0. Offline-first core stays the recommended starting point (`python examples/core_mvp_agent.py`).

## [0.51.0] - 2026-10-13

### Added
- Clean core MVP entry point: `examples/core_mvp_agent.py` — one script demonstrates offline intent routing, file ops, calculator, system info, web search fixture, and MCP echo with multi-LLM provider probes.
- Improved intent keywords in MVP router for more reliable tool selection.
- README: vivid GIF/storyboard descriptions for the core demos + reinforced 1-command install.
- Public roadmap and CONTRIBUTING notes refreshed for the MVP.

### Changed
- Version bump to 0.51.0. Core offline path remains the recommended starting point.

## [0.50.0] - 2026-10-12

### Added
- Enhanced offline core: improved math expression extraction in MVP intent routing.
- Ready-to-run examples: `examples/enhanced_chat_agent.py` (offline fallback + multi-LLM probes) and `examples/enhanced_automation_agent.py` (full automation without a model).
- README updates: clearer one-command path, new GIF storyboards, expanded examples table.
- Docs: `docs/HN_UPDATE_v050.md` for HN / Indie Hackers.

### Changed
- Version bump; core MVP remains the recommended first demo.

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
