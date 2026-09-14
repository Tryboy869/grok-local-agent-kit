# HN / Indie Hackers update — v0.27.0 (2026-09-14)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools (files, web, MCP), workspace RAG, and a tools demo that runs with no LLM.

## What's new this week
- Web search no longer dies when `duckduckgo-search` is missing or rate-limited — HTML fallback.
- `grok-agent tools list|demo` and `examples/tools_demo_agent.py` so first-run is not blocked on Ollama.
- README: 1-command install, example table, ASCII storyboard (GIFs still recorded locally — see `docs/gifs/README.md`).

## Indie Hackers angle
Ship agents that work on a laptop without an API bill. The interesting loop is: tools + router + cwd-safe files + MCP. Cloud is optional.

## Ask
If you run local models, what is the first tool you actually trust an agent with? Files? Shell? MCP?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
