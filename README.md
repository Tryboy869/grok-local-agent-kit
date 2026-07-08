# 🧠 grok-local-agent-kit

**Open-source toolkit for building powerful local AI agents with MCP support, multi-LLM routing, and developer tools. Run agents offline-first. Built autonomously by Grok.**

![Stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)
![Forks](https://img.shields.io/github/forks/Tryboy869/grok-local-agent-kit?style=social)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![PyPI](https://img.shields.io/pypi/v/grok-local-agent-kit)](https://pypi.org/project/grok-local-agent-kit/)

## ✨ Features

- **Offline-first with Ollama**: Support for Llama, Mistral, Gemma, Phi etc.
- **MCP Protocol**: Advanced multi-context processing for agent collaboration.
- **Autonomous Agents**: Planning, tool use, reflection.
- **Tool Integration**: File ops, code exec, web search (via APIs).
- **Multi-Agent Orchestration**: Teams of specialized agents.
- **CLI + Python Library**: Easy integration.
- **Extensible**: Custom skills and plugins.
- **CI/CD Ready**: GitHub Actions included.

## 🚀 Quick Start

1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Pull a model: `ollama pull llama3.2`
3. Install kit: `pip install grok-local-agent-kit`
4. Run: `grok-local-agent-kit chat "Your prompt here"`

## 📦 Installation

```bash
pip install grok-local-agent-kit
```

## 📖 Usage

```python
from grok_local_agent_kit.agent import Agent

agent = Agent(model="llama3.2")
print(agent.chat("Hello world!"))
```

See `examples/` for more.

## 🛣️ Roadmap

See [ROADMAP.md](ROADMAP.md)

## 🤝 Contributing
Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📜 License
MIT - see [LICENSE](LICENSE)

**Star ⭐ if useful! Goal: 10k stars in 3 months.** Built with ❤️ by Grok.