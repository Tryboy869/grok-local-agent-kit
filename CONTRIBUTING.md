# Contributing to grok-local-agent-kit

Thanks for helping make local AI agents better.

## Quick start for contributors

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
pytest -q
```

## Development workflow

1. Fork & create a branch: `git checkout -b feature/your-idea`
2. Make changes + add tests if possible
3. Lint & format (`ruff check --fix .` and `black .`)
4. Run tests: `pytest`
5. Commit with conventional messages (`feat:`, `fix:`, `docs:`)
6. Open a Pull Request against `main`

## What we need most (priority order)

1. True sqlite-vec vec0 writes (v0.23 already probes + falls back)
2. Live-model opt-in eval cases (Ollama)
3. Vision support (local multimodal models)
4. Demo GIFs / asciinema recordings (`docs/gifs/`)
5. Windows & macOS packaging notes
6. Additional examples and skill packs
7. PyPI-stable 1.0 API freeze

v0.23 ships an optional sqlite-vec backend (`grok-agent vec`) with hash fallback.
v0.22 ships tool-call budgets and a retry helper on top of the v0.21 cache/telemetry stack.
v0.20 shipped MCP session ids + request cancel and an offline eval harness.
v0.19 shipped a workspace watcher, JSON extract, and LLM-free TOML recipes.
v0.18 shipped process-group kill on `run_shell` timeout/cancel.

## Code style

- Python 3.10+
- Type hints encouraged
- Keep the core dependency surface small (stdlib first)
- No live LLM required for unit tests
- Default network binds to loopback. Do not change `serve` to `0.0.0.0` without an explicit flag and a warning.

Thank you!
