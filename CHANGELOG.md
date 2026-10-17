## [0.54.0] - 2026-10-17

### Added
- Clearer multi-LLM routing documentation and provider health probes for Ollama + LM Studio in the core agent path.
- Ready-to-run examples reinforced: `examples/chat_agent.py` (interactive ReAct) and `examples/automation_agent.py` (one-shot tool goal).
- README: one-command install front-and-center, vivid GIF/storyboard descriptions for chat and automation demos.
- Public CONTRIBUTING.md and ROADMAP.md kept current; new HN/Indie Hackers update draft.

### Changed
- Version bump to 0.54.0. Offline-first MVP remains the recommended starting point (`python examples/core_mvp_agent.py` or `grok-agent mvp`).

## [0.53.0] - 2026-10-15

### Added
- More robust math expression extraction in the offline MVP router (strips leading verbs, extracts first math-like substring).
- Continued polish of the core offline path so `python examples/core_mvp_agent.py` and enhanced examples stay reliable with zero models.
- Docs: `docs/HN_UPDATE_v053.md` prepared for Hacker News / Indie Hackers.

### Changed
- Version bump to 0.53.0. Offline-first core remains the recommended starting point.
