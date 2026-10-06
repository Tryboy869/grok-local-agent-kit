# Update — HN / Indie Hackers (v0.45)

## Show HN title

Show HN: grok-local-agent-kit – offline-first local agents (Ollama, LM Studio, MCP)

## HN body

I have been building a small Python kit for local agents that does not need a cloud key.

v0.45 adds a path you can run with zero models installed:

- `grok-agent mvp` routes a goal to file tools, a calculator, web search (injectable), system info, or an MCP echo
- Ollama (`127.0.0.1:11434`) and LM Studio (`127.0.0.1:1234/v1`) are probed; if they are down the demo still finishes
- Live chat is still there: `grok-agent chat --router` when a local model is up

Install: `curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash`

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Looking for feedback on the tool surface and whether the scripted MVP should hand off to ReAct automatically when a backend is up.

## Indie Hackers

**Title:** Local agent kit that demos with no API key and no model

**Post:**

Shipped v0.45 of grok-local-agent-kit. The pitch is simple: agents that stay on the machine.

What is new:

- One command install
- `grok-agent mvp` — intent routing + real file/math/search tools, no daemon
- Examples: `examples/mvp_chat.py`, `examples/mvp_automation.py`
- Same package already speaks Ollama, LM Studio, and MCP when you want a live model

I am not charging for it (MIT). Next step is a 30s GIF and an automatic handoff from the scripted plan to the live tool loop when Ollama answers.

https://github.com/Tryboy869/grok-local-agent-kit
