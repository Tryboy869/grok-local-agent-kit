## [0.77.0] - 2026-11-19

### Added
- Offline MVP now supports compound “system info and save” goals: get_system_info result is automatically injected into a subsequent write_file.
- New ready-to-run example `examples/ready_local_agent_v077.py` demonstrating system→file, datetime→file, code→file, search→file, math, and workspace listing — fully offline.
- Clearer demo storyboards mentioning system-to-file chaining.

### Changed
- Version bump to 0.77.0.
- Offline demos now exercise real result injection for system_info→file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update).

## [0.76.0] - 2026-11-18

### Added
- Offline MVP now supports compound “datetime / current time and save” goals: get_datetime result is automatically injected into a subsequent write_file.
- More robust previous-result injection into write_file (additional placeholders + empty content handling).
- New ready-to-run example `examples/ready_local_agent_v076.py` demonstrating datetime→file, code→file, search→file, math, system info, and workspace listing — fully offline.
- Clearer demo storyboards mentioning datetime-to-file chaining.

### Changed
- Version bump to 0.76.0.
- Offline demos now exercise real result injection for datetime→file multi-step plans.
- Docs synced.
