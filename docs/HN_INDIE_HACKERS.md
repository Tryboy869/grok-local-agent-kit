# HN / Indie Hackers update — v0.29.0 (2026-09-16)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools, workspace RAG, multi-agent teams — and now the shared blackboard survives process restarts as JSONL or SQLite. Demos still run with zero cloud and zero LLM.

## What's new this week
- Persist `Blackboard` to JSONL (default) or SQLite.
- `grok-agent board demo|show` and `examples/persist_agent.py`.
- Reload a previous team run, then append another round.

## Indie Hackers angle
Coordination state is usually trapped in RAM or a vendor dashboard. This kit writes the same posts you already see in `team demo` to a file in the workspace, so overnight runs and cron jobs can resume without a hosted queue.

## Ask
Would you rather we ship a 20s terminal GIF next, or a Test PyPI package?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
