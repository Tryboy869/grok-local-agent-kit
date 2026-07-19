# 🚀 Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)

**MVP toolkit for autonomous local AI agents. Supports Ollama, LM Studio, routing, tools (web/file/MCP), multi-LLM. Fully offline capable.**

## ✨ Features
- Core agent with tool calling & reasoning
- Multi-provider LLM (Ollama + LM Studio)
- Tools: web_search, file ops, list_files, MCP
- Ready examples: chat, automation
- CLI support

## 1-Command Install & Run

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git ollama duckduckgo-search

ollama pull llama3.2

# Run example
python -m grok_local_agent_kit.run_agent  # or use examples/
```

## Demos

**Chat Agent**:
```bash
python examples/chat_agent.py
```

**Automation Agent** (file creation, etc.):
```bash
python examples/automation_agent.py
```

*GIF Demo Descriptions:*
1. **Terminal Chat**: User inputs task → Agent reasons → Calls web_search tool → Returns summarized results (animated loop).
2. **File Ops**: Prompt "create report.md" → Tool write → Confirmation + ls command output.
3. **Routing**: Complex query auto-routes to file/web handlers.

## CLI
`grok-agent chat "Your idea" --model llama3.2`

## Contributing & Roadmap
See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).

Built with ❤️ by Grok in autonomous dev mode.