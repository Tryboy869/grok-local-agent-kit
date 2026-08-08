# Contributing to grok-local-agent-kit

Thanks for helping make local AI agents better.

## Quick start for contributors

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
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

1. **Real MCP client** (stdio / SSE) — highest priority for v0.8
2. More robust tool sandboxing (especially `execute_python` & `run_shell`)
3. Streaming responses from the LLM
4. Memory / conversation persistence beyond JSON
5. Vision support (local multimodal models)
6. Better error messages & structured logging
7. Demo GIFs / recordings for the README
8. Windows & macOS packaging notes
9. Additional ready-to-run examples
10. CI coverage for more edge cases

## Code style

- Python 3.10+
- Type hints encouraged
- Keep the core dependency surface small
- Prefer clarity over cleverness
- No live LLM required for unit tests

## Reporting issues

Open an issue with:
- OS + Python version
- LLM provider & model
- Minimal reproduction steps
- Expected vs actual behavior

Thank you! 🧠
