# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.14.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)

**Open-source toolkit for building local AI agents.**  
Ollama + LM Studio • ReAct tool loop • multi-LLM fallback router • JSONL + **SQLite vector memory** • **optional Ollama embeddings** • **on_thought** • **sandboxed execute_python** • skill packs • orchestrator • MCP stdio / HTTP / **SSE with retry** • MCP **prompts** • file config • hooks + **token usage** • offline-first.  
Built autonomously by Grok.

> Capable agents on your machine. No cloud required. No API keys for local models.

## ✨ Features (v0.14.0)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compat / LM Studio) | ✅ |
| Fallback router (`MultiLLMRouter`, `grok-agent route`, `--router`) | ✅ |
| ReAct-style tool calling loop | ✅ |
| Streaming final answers + `on_token` hook | ✅ |
| File / web / shell / Python / calculator / MCP tools | ✅ |
| Memory tools (`remember` / `recall` / `forget`) + CLI | ✅ |
| SQLite vector memory (`vremember` / `vrecall`) | ✅ |
| Optional Ollama embeddings (`GROK_EMBED_BACKEND=ollama`) | ✅ |
| `on_thought` hook during the tool loop | ✅ |
| Restricted `execute_python` sandbox + timeout | ✅ |
| Cheap usage tracker (`agent.usage.summary()`) | ✅ |
| Skill packs (`.grok/skills/*.json`) | ✅ |
| Hook bus wired into the live ReAct loop + `last_trace` | ✅ |
| Orchestrator (planner + researcher / coder / operator) | ✅ |
| MCP stdio JSON-RPC + auto-register discovered tools | ✅ |
| MCP HTTP JSON-RPC + SSE client with reconnect | ✅ |
| MCP prompts (`prompts/list`, `prompts/get`) | ✅ |
| Named sessions under `.grok/sessions/` | ✅ |
| `grok-agent.toml` / JSON config (`grok-agent init`) | ✅ |
| CLI + examples + unit tests (no live LLM required) | ✅ |

## 🎬 Demo GIFs (record with asciinema / VHS)

Drop recordings into `docs/gifs/` when you have a terminal handy:

1. `demo-chat.gif` — `grok-agent chat -v --stream`
2. `demo-route.gif` — `grok-agent route`
3. `demo-mcp.gif` — `python examples/mcp_agent.py --no-llm`
4. `demo-hooks.gif` — `python examples/hooks_agent.py`
5. `demo-memory.gif` — `grok-agent memory remember "ship v0.14"` then `recall ship`
6. `demo-vector.gif` — `python examples/vector_memory_agent.py`
7. `demo-skills.gif` — `python examples/skills_agent.py`
8. `demo-sandbox.gif` — `python examples/sandbox_agent.py`
9. `demo-embed.gif` — `python examples/embed_agent.py`

Storyboard: [docs/gifs/README.md](docs/gifs/README.md). Until binary GIFs land, the commands above are the live demo.

## ⚡ Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent init
grok-agent route
grok-agent chat -v --stream --router
```

Or:

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
```

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
pytest -q
```

Needs Python 3.10+ and Ollama or LM Studio. `ollama pull llama3.2` is a good default.

```python
from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", provider="ollama", use_router=True, verbose=True)

def log_tool(*, name, args, **_):
    print("calling", name, args)

agent.on("before_tool", log_tool)
agent.on("on_thought", lambda **p: print("thought:", p.get("text", "")[:200]))
agent.on("on_token", lambda **p: print(p.get("text", ""), end=""))
agent.load_skills()
print(agent.run("List files and remember that this workspace is the kit repo"))
print(agent.last_trace)
print(agent.usage.summary())
agent.close()
```

## Examples

```bash
python examples/chat_agent.py
python examples/automation_agent.py
python examples/mcp_agent.py --no-llm
python examples/memory_agent.py
python examples/vector_memory_agent.py
python examples/orchestrator_agent.py --no-llm
python examples/hooks_agent.py
python examples/config_agent.py
python examples/skills_agent.py
python examples/sandbox_agent.py
python examples/embed_agent.py
```

## Config

`grok-agent init` writes `grok-agent.toml`. Env vars still win:

- `GROK_AGENT_MODEL`, `GROK_AGENT_PROVIDER`, `GROK_AGENT_BASE_URL`
- `GROK_AGENT_ROUTER=1`
- `GROK_AGENT_CONFIG=/path/to/file`
- `GROK_EMBED_BACKEND=hash|ollama` and `GROK_EMBED_MODEL=nomic-embed-text`

## Roadmap / contributing / license

See [ROADMAP.md](ROADMAP.md), [CONTRIBUTING.md](CONTRIBUTING.md), [LICENSE](LICENSE).

Launch drafts: [SHOW_HN.md](SHOW_HN.md) · [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

Built autonomously by Grok · Nexus Studio / Tryboy869  
https://github.com/Tryboy869/grok-local-agent-kit
