# HN / Indie Hackers update — v0.33.0 (2026-09-20)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools, workspace RAG, multi-agent teams — and now the file-backed approval gate actually sits on the tool loop. A denied or still-pending tool never runs; the model just sees a block message.

## What's new this week
- v0.32: `ApprovalGate` allow/deny lists + JSON persist.
- v0.33: `Agent(approval_gate=...)` + `attach_approval_gate` + `gated_execute`. `HookBus` re-raises `ApprovalDenied`. `grok-agent approve react` simulates a ReAct batch with zero LLM.

## Indie Hackers angle
Most kits either auto-run every tool or bounce you through a hosted dashboard. This one writes pending approvals next to the workspace and refuses the tool until a human (or a local decider) says yes.

## Draft post
**Title:** Show HN: local-first agent kit that blocks tools until you approve them (no cloud queue)

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent approve demo
grok-agent approve react
python examples/react_approve_agent.py
```

Calculator runs. `run_shell` is denied. `web_search` stays pending. Decisions land in `approvals.json`.

Ask: Test PyPI next, or a 20s terminal GIF?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
