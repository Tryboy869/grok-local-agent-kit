# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.11.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)

**Open-source toolkit for building local AI agents.**  
Ollama + LM Studio • ReAct tool loop • multi-LLM fallback router • JSONL memory • orchestrator • MCP stdio **and HTTP** • file config • event hooks • offline-first.  
Built autonomously by Grok.

> Capable agents on your machine. No cloud required. No API keys for local models.

## ✨ Features (v0.11.0)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compat / LM Studio) | ✅ |
| Fallback router (`MultiLLMRouter`, `grok-agent route`, `--router`) | ✅ |
| ReAct-style tool calling loop | ✅ |
| Streaming final answers | ✅ |
| File / web / shell / Python / calculator / MCP tools | ✅ |
| Local JSONL memory (`remember` / `recall` / `forget`) | ✅ |
| Orchestrator (planner + researcher / coder / operator) | ✅ |
| MCP stdio JSON-RPC + auto-register discovered tools | ✅ |
| **MCP HTTP JSON-RPC client** (`HTTPMCPClient`, `grok-agent mcp-http`) | ✅ |
| Named sessions under `.grok/sessions/` | ✅ |
| **`grok-agent.toml` / JSON config** (`grok-agent init`) | ✅ |
| **Event hooks** (`before_tool`, `after_tool`, `on_final`, …) | ✅ |
| CLI + examples + unit tests (no live LLM required) | ✅ |

## 🎬 Demo GIFs (record with asciinema / VHS)

Drop recordings into `docs/gifs/` when you have a terminal handy:

1. `demo-chat.gif` — `grok-agent chat -v --stream`  
   *What you should see:* Rich prompt, tool arrows (`→ calculator`), streamed final answer.
2. `demo-route.gif` — `grok-agent route`  
   *What you should see:* Ollama probed first, LM Studio second, `active:` line.
3. `demo-mcp.gif` — `python examples/mcp_agent.py --no-llm`  
   *What you should see:* bundled echo server tools listed without a GPU.
4. `demo-hooks.gif` — `python examples/hooks_agent.py`  
   *What you should see:* `before_tool` / `after_tool` printed for `calculator`.
5. `demo-memory.gif` — `grok-agent memory remember "ship v0.11"` then `recall ship`

Until GIFs land, the commands above are the live demo.

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
print(agent.run("List files and remember that this workspace is the kit repo"))
agent.close()
```

## Examples

```bash
python examples/chat_agent.py
python examples/automation_agent.py
python examples/mcp_agent.py --no-llm
python examples/memory_agent.py
python examples/orchestrator_agent.py --no-llm
python examples/hooks_agent.py
python examples/config_agent.py
```

## Config

`grok-agent init` writes `grok-agent.toml`. Env vars still win:

- `GROK_AGENT_MODEL`, `GROK_AGENT_PROVIDER`, `GROK_AGENT_BASE_URL`
- `GROK_AGENT_ROUTER=1`
- `GROK_AGENT_CONFIG=/path/to/file`

## Roadmap / contributing / license

See [ROADMAP.md](ROADMAP.md), [CONTRIBUTING.md](CONTRIBUTING.md), [LICENSE](LICENSE).

Launch drafts: [SHOW_HN.md](SHOW_HN.md) · [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

Built autonomously by Grok · Nexus Studio / Tryboy869  
https://github.com/Tryboy869/grok-local-agent-kit
