## [0.79.0] - 2026-11-21

### Added
- Offline MVP now supports compound “fetch URL and save” goals: http_get result is automatically injected into a subsequent write_file.
- New ready-to-run example `examples/ready_local_agent_v079.py` demonstrating http→file, math→file + verification, system→file, datetime→file, code→file, search→file, and workspace listing — fully offline.
- Clearer demo storyboards mentioning http-to-file chaining.

### Changed
- Version bump to 0.79.0.
- Offline demos now exercise real result injection for http_get→file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update).

## [0.78.0] - 2026-11-20

### Added
- Offline MVP now supports improved compound “calculate and save” goals: calculator result is automatically injected into write_file, with optional read-back verification step when the goal mentions “verify” / “read back”.
- New ready-to-run example `examples/ready_local_agent_v078.py` demonstrating math→file + verification, system→file, datetime→file, code→file, search→file, and workspace listing — fully offline.
- Clearer demo storyboards mentioning math-to-file chaining with verification.

### Changed
- Version bump to 0.78.0.
- Offline demos now exercise real result injection for math→file multi-step plans + verification.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update, STATUS).

## [0.77.0] - 2026-11-19

### Added
- Offline MVP now supports compound “system info and save” goals: get_system_info result is automatically injected into a subsequent write_file.
- New ready-to-run example `examples/ready_local_agent_v077.py` demonstrating system→file, datetime→file, code→file, search→file, math, and workspace listing — fully offline.
- Clearer demo storyboards mentioning system-to-file chaining.

### Changed
- Version bump to 0.77.0.
- Offline demos now exercise real result injection for system_info→file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update).
