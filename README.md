# 🚀 Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)

**Open-source toolkit for building powerful local AI agents. Supports Ollama, MCP, multi-LLM routing, tools, and offline-first execution. Built autonomously by Grok for developers.**

## ✨ Features
- **Autonomous Agents**: Tool-calling, reasoning loops, multi-step tasks
- **Local LLMs**: Ollama, LM Studio, OpenAI-compatible endpoints
- **MCP Support**: Shared context/memory for multi-agent systems
- **Rich Tools**: Web search, file I/O, directory listing, custom tools
- **CLI & Examples**: Ready-to-run chat and automation agents
- **Extensible**: Easy tool registration and routing
- **CI/CD**: GitHub Actions for testing

## Quickstart

```bash
# Install
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
pip install ollama duckduckgo-search

# Pull model
ollama pull llama3.2

# Run CLI
grok-agent chat "Plan a simple web scraper agent"

# Or Python
python -c '
from grok_local_agent_kit.agent import create_agent
agent = create_agent()
print(agent.chat("List files and search for AI agent tutorials"))
'
```

## Project Structure
```
grok-local-agent-kit/
├── grok_local_agent_kit/   # Core package
│   ├── agent.py            # Main Agent class
│   ├── cli.py              # Command line interface
│   ├── tools.py            # Tool utilities
│   └── ...
├── examples/               # Demos
├── .github/workflows/      # CI
├── pyproject.toml          # Modern packaging
└── README.md
```

## Roadmap
See [ROADMAP.md](ROADMAP.md)

## License
MIT - see [LICENSE](LICENSE)

Built with ❤️ autonomously by Grok to empower local AI development. Star ⭐ if it helps you!