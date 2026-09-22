# Contributing

Thanks for helping build local-first agents.

## Setup

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Rules of the road

- Python 3.10+, no required cloud APIs.
- New behavior needs tests that run **without a live LLM**.
- Keep the public surface in `grok_local_agent_kit/__init__.py` intentional.
- Prefer small modules (`cli_v0XX.py`, `test_v0XX.py`) over growing god-files.
- File tools stay workspace-scoped. Do not weaken `_safe_path`.
- Blackboard, roster, handoff, and approval persistence stay cwd-safe.
- ApprovalGate checks on the ReAct path must fail closed (block on deny **and** pending).
- Approval TUI scripts must stay offline-testable (`--script` / `--policy`); do not require a TTY in tests.
- Live-model eval stays **opt-in**. Default and CI paths use the stub. Real models require both `--live` and `GROK_LIVE_EVAL=1`.
- Do not load untrusted Python plugins by default. JSON plugins are data-only.
- Workspace packer / file RAG must stay cwd-safe and skip VCS / venv trees.
- Do not commit secrets, model weights, or large binaries.

## Pull requests

1. Open an issue if the change is bigger than a small fix.
2. One concern per PR.
3. Update `CHANGELOG.md` and bump version in `pyproject.toml` + `__init__.py` when you add a feature.
4. Run `pytest -q` and `ruff check grok_local_agent_kit tests` if you have ruff.

## Code of conduct

See `CODE_OF_CONDUCT.md`. Security reports: `SECURITY.md`.
