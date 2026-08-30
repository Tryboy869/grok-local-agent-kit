# Show HN: Grok Local Agent Kit — offline agents with tools, MCP, and LLM fallback

I built a small Python kit so you can run a tool-using agent on your laptop with Ollama or LM Studio. No cloud key required.

Most agent stacks assume OpenAI/Anthropic. I wanted something that:

- works fully offline with local models
- actually calls tools (files, shell, Python, web, calculator)
- talks to MCP servers over stdio JSON-RPC
- falls back from Ollama to LM Studio if one is down
- keeps memory in a local JSONL file

**What it does**

- ReAct loop with cwd-safe file tools
- Real MCP stdio client + auto-register discovered tools
- Fallback router: try Ollama, then LM Studio
- JSONL memory (`remember` / `recall` / `forget`)
- Tiny orchestrator (planner + researcher / coder / operator)
- CLI: `grok-agent doctor | route | chat | memory`

**Try it**

    pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
    grok-agent doctor
    grok-agent route
    grok-agent chat -v --stream --router

From source:

    git clone https://github.com/Tryboy869/grok-local-agent-kit.git
    cd grok-local-agent-kit && pip install -e ".[dev]" && pytest -q

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Feedback welcome — especially on MCP HTTP/SSE (issue #2) and a recorded demo (issue #1).
