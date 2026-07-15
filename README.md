# Grok Local Agent Kit

[![Stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org) [![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)

**Open-source toolkit for building powerful local AI agents.** Run agents offline-first with Ollama, LM Studio, MCP support, multi-LLM routing, and developer tools. Built with ❤️ by Grok and the community.

## ✨ Features

- **Local-first**: Full offline support with Ollama & LM Studio
- **Tool Integration**: Web search, file I/O, custom tools
- **MCP Support**: Memory, Context, Planning for advanced agents
- **Multi-Provider**: Ollama, OpenAI-compatible (LM Studio, etc.)
- **CLI & Python API**: Easy to use and extend
- **Extensible**: Add your own tools and agents

## 🚀 Quickstart

```bash
pip install grok-local-agent-kit

# Run CLI
grok-agent "Plan a local AI agent for coding assistance"

# Python
from grok_local_agent_kit.agent import create_agent

agent = create_agent(model="llama3.2")
print(agent.chat("Hello, what can you do?"))
```

## 📖 Documentation

See [ROADMAP.md](ROADMAP.md) and examples/.

## 🛠️ Installation

```bash
pip install -e .[dev]
```

Ensure Ollama is running: `ollama serve` and pull models.

## Roadmap

- v0.3: Advanced MCP, agent orchestration
- v1.0: GUI, more integrations

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
MIT - see [LICENSE](LICENSE)

---

*Autonomously initialized by Grok for massive open-source impact. Aim: 10k stars in 3 months!*
