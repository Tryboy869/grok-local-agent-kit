# Show HN: Grok Local Agent Kit — offline agents with tools, MCP, hooks, and LLM fallback

I built a small Python kit so you can run a tool-using agent on your laptop with Ollama or LM Studio. No cloud key required.

**What it does (v0.11)**

- ReAct loop with cwd-safe file tools
- Real MCP stdio client and a minimal MCP HTTP JSON-RPC client
- Fallback router: try Ollama, then LM Studio
- JSONL memory (`remember` / `recall`)
- Tiny orchestrator (planner + specialists)
- `grok-agent.toml` config + event hooks

**Try it**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent route
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
