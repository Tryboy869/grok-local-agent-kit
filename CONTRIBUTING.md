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
3. Lint & format:
   ```bash
   ruff check --fix .
   black .
   ```
4. Run tests: `pytest`
5. Commit with a clear message (conventional commits preferred):
   - `feat: ...`
   - `fix: ...`
   - `docs: ...`
6. Open a Pull Request against `main`

## What we need most (priority order)

1. Full MCP Streamable HTTP + SSE reconnection
2. MCP prompts + richer resource templates
3. Stronger tool sandboxing (`execute_python` & `run_shell`)
4. Token-level streaming inside the tool loop
5. Optional vector memory (sqlite-vec)
6. Vision support (local multimodal models)
7. Demo GIFs / asciinema recordings for the README (`docs/gifs/`)
8. Windows & macOS packaging notes
9. Additional ready-to-run examples and skill packs
10. CI coverage for more edge cases

## Code style

- Python 3.10+
- Type hints encouraged (`py.typed` is present)
- Keep the core dependency surface small
- Prefer clarity over cleverness
- No live LLM required for unit tests (use a FakeLLM)

## Reporting issues

Open an issue with:

- OS + Python version
- LLM provider & model
- Minimal reproduction steps
- Expected vs actual behavior

Thank you! 🧠
