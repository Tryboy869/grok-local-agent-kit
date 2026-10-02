# Show HN: grok-local-agent-kit

Local-first Python toolkit for AI agents. Ollama + LM Studio, ReAct tools, workspace RAG, multi-agent teams, a file-backed approval TUI, opt-in live eval, a circuit breaker on the multi-LLM router that survives process restart, a portable kit snapshot, a local model catalog, and a **router that adopts the models actually installed on the box**.

**What it does**

- Talks to Ollama or LM Studio (OpenAI-compat) with a multi-LLM fallback router
- `HealthBoard` on `pick` / `probe` / `chat`: open breakers are not pinged
- Routed decisions persist to the same `health.json` the health CLI uses
- `grok-agent snapshot demo` writes `kit-snapshot.json`
- `grok-agent models demo` writes `catalog.json` (Ollama tags + LM Studio /v1/models)
- `grok-agent route catalog` rewrites endpoint models via `Catalog.pick`
- ReAct tool loop: files, web, shell, calculator, Python sandbox, MCP (stdio / HTTP / SSE)
- A local approval gate sits on that loop: denied or pending tools never execute
- Scriptable TUI: `grok-agent approve tui --script A003=approved,A004=denied`
- Opt-in live eval: `grok-agent eval-demo` (stub) or `GROK_LIVE_EVAL=1 grok-agent eval-live --live`
- Health + route + snapshot + catalog demos need **zero** live chat
- Web search that still works if the DDG Python package flakes (HTML fallback)
- Workspace packer + local file RAG — no network
- Multi-agent `Team` with a shared blackboard, persisted roster, handoff queue
- Drop-in plugins: JSON tools always load; Python plugins are opt-in only
- Local HTTP API, SQLite memory (optional sqlite-vec), eval harness, budgets, transcripts

**Try it**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent models demo
grok-agent route catalog
grok-agent snapshot demo
grok-agent eval-demo
grok-agent health demo
grok-agent route demo
grok-agent route persist
grok-agent approve tui --seed --script A003=approved,A004=denied
```

Chat needs Ollama or LM Studio:

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit


## Follow-up (v0.43, 2026-10-02)

Show HN: Local agent kit – JSON workflows for files, search, and MCP (no daemon)

`grok-agent workflow demo` runs four real steps offline. Chat/automation examples still target Ollama or LM Studio when you want a model. One-command install via `scripts/install.sh`. GIF storyboard: `docs/gifs/workflow-demo.md`.
