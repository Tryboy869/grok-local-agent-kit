# HN / Indie Hackers update — v0.35.0 (2026-09-22)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools, workspace RAG, multi-agent teams, scriptable approval TUI, and an opt-in live-model eval profile that stays stubbed in CI.

## What's new this week
- v0.34: `grok-agent approve tui|queue`. Script `A003=approved,A004=denied`.
- v0.35: `grok-agent eval-demo` / `eval-live`. Default path is a deterministic stub. Real models need `--live` **and** `GROK_LIVE_EVAL=1`.

## Indie Hackers angle
You can ship an eval suite with the kit without forcing every contributor to own a GPU. When you *do* have Ollama running, flip one env var and score the same cases against a real model.

## Draft post
**Title:** Show HN: local-first agent kit + opt-in live eval (CI stays offline)

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent eval-demo
grok-agent approve tui --seed --script A003=approved,A004=denied
python examples/live_eval_agent.py
# optional:
# GROK_LIVE_EVAL=1 grok-agent eval-live --live
```

Ask: Test PyPI next, or a 20s terminal GIF?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
