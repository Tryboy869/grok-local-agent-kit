# HN / Indie Hackers update — v0.41.0 (2026-09-30)

## One-liner
Local-first Python agent kit: the multi-LLM router now uses the models actually installed on your machine (`Catalog.pick` → endpoint.model), not a hardcoded `llama3.2` / `local-model`.

## What's new this week
- v0.40: `grok-agent models demo` writes `catalog.json`.
- v0.41: `grok-agent route catalog` rewrites router defaults from that catalog. Offline demo, no chat process.

## Indie Hackers angle
Support ticket #1 after "is Ollama running?" is "why is it calling llama3.2 when I only pulled qwen?". The catalog + router binding closes that loop.

## Draft post
**Title:** Show HN: local agent kit — router picks the model you actually installed

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent models demo
grok-agent route catalog
python examples/catalog_route_agent.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Ask: Test PyPI next, or recorded GIFs?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
