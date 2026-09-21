# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.34.0] — 2026-09-21

### Added
- Scriptable approval TUI (`approve_tui`): parse `A003=approved,A004=denied`, bulk policies
- CLI: `grok-agent approve tui|queue` (no live LLM)
- Example: `examples/approve_tui_agent.py`
- Tests: `tests/test_v034.py`

## [0.33.0] — 2026-09-20

### Added
- Wire `ApprovalGate` into the ReAct tool path (`react_gate.attach_approval_gate`, `gated_execute`)
- `Agent(..., approval_gate=gate)` attaches a `before_tool` listener; denied tools become a block message
- `HookBus.emit` re-raises `ApprovalDenied` so HITL can stop a tool mid-loop
- CLI: `grok-agent approve react` (no live LLM)
- Example: `examples/react_approve_agent.py`
- Tests: `tests/test_v033.py`

## [0.32.0] — 2026-09-19

### Added
- Local approval gate (`ApprovalGate`, `Approval`, `ApprovalDenied`)
- Allow / deny lists + programmable decider + persist JSON
- CLI: `grok-agent approve demo|show` (no live LLM)
- Example: `examples/approve_agent.py`
- Tests: `tests/test_v032.py`

## [0.31.0] — 2026-09-18

### Added
- Task handoff queue (`HandoffQueue`, `Task`, `save_queue` / `load_queue`)
- Offer / claim / complete / drop with optional Blackboard mirror
- JSON + SQLite persistence (cwd-safe)
- CLI: `grok-agent handoff demo|show` (no live LLM)
- Example: `examples/handoff_agent.py`
- Tests: `tests/test_v031.py`

### Changed
- README features heading aligned to current version
- Public exports for handoff helpers
