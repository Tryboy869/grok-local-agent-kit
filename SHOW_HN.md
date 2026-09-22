# Show HN: grok-local-agent-kit

Local-first Python toolkit for AI agents. Ollama + LM Studio, ReAct tools, workspace RAG, multi-agent teams, a file-backed approval TUI, and an opt-in live-model eval profile that stays stubbed unless you flip `GROK_LIVE_EVAL=1`.

**What it does**

- Talks to Ollama or LM Studio (OpenAI-compat) with a multi-LLM fallback router
- ReAct tool loop: files, web, shell, calculator, Python sandbox, MCP (stdio / HTTP / SSE)
- A local approval gate sits on that loop: denied or pending tools never execute
- Scriptable TUI: `grok-agent approve tui --script A003=approved,A004=denied`
- Opt-in live eval: `grok-agent eval-demo` (stub) or `GROK_LIVE_EVAL=1 grok-agent eval-live --live`
- Web search that still works if the DDG Python package flakes (HTML fallback)
- Workspace packer + local file RAG — no network
- Multi-agent `Team` with a shared blackboard, persisted roster, handoff queue
- Drop-in plugins: JSON tools always load; Python plugins are opt-in only
- Local HTTP API, SQLite memory (optional sqlite-vec), eval harness, budgets, transcripts
- Demos (`tools`, `team`, `roster`, `handoff`, `approve`, `eval-demo`) run with **zero** live model

**Try it**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent eval-demo
grok-agent approve tui --seed --script A003=approved,A004=denied
```

Chat needs Ollama or LM Studio:

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
