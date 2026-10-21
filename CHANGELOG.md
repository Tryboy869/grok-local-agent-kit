## [0.58.0] - 2026-10-21

### Added
- Enhanced core agent example: `examples/enhanced_core_agent.py` — smarter offline routing, clearer multi-tool chain (datetime, math, files, search fixture, system, MCP), multi-LLM probes.
- Improved intent handling notes and demo storyboard in README.

### Changed
- Version bump to 0.58.0. Offline-first core remains the recommended entry point.


## [0.57.0] - 2026-10-20

### Added
- Datetime intent routing in the offline MVP core (`route_intent` / `plan_for`) — keywords for time/date trigger `get_datetime`.
- New ready-to-run multi-tool example: `examples/ready_multi_tool_agent.py` — chains datetime, math, files, search fixture, and system info. Fully offline, includes multi-LLM probes.
- README / docs: updated examples table and GIF storyboard notes for the multi-tool demo.

### Changed
- Version bump to 0.57.0. Offline demos remain the recommended starting point.

## [0.56.0] - 2026-10-19

### Added
- Polished core MVP agent path with clearer intent routing and multi-tool demos.
- New ready-to-run examples: `examples/ready_chat_agent.py` and `examples/ready_automation_agent.py` (offline-first, tools + multi-LLM probes).
- README: reinforced 1-command install, vivid GIF/storyboard descriptions for core/chat/automation demos, expanded examples table.
- Updated CONTRIBUTING.md and public ROADMAP.md; prepared HN/Indie Hackers update for v0.56.

### Changed
- Version bump to 0.56.0. Recommended entry point remains offline: `python examples/core_agent_demo.py` or the new ready examples.

## [0.55.0] - 2026-10-18

### Added
- Enhanced core agent routing in MVP path (expanded keywords, better math detection, trace alias).
- New ready-to-run example: `examples/core_agent_demo.py` — demonstrates routing + web search, file ops, calculator, system info, MCP echo + multi-LLM probes. Fully offline.
- README updates: version badge, new GIF storyboard description, one-command install reinforced, examples table.
- Public roadmap and CONTRIBUTING kept current; HN/Indie Hackers update prepared.

### Changed
- Version bump to 0.55.0. Offline-first core remains the recommended starting point (`python examples/core_agent_demo.py`).
