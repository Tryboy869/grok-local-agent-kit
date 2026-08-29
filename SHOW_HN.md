# Show HN: Grok Local Agent Kit — offline agents with tools, MCP, and LLM fallback

I built a small Python kit so you can run a tool-using agent on your laptop with Ollama or LM Studio. No cloud key required.

**What it does**

- ReAct loop with cwd-safe file tools
- Real MCP stdio client
- Fallback router: try Ollama, then LM Studio
- JSONL memory (`remember` / `recall`)
- Tiny orchestrator (planner + specialists)

**Try it**

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent route
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
