# 🧠 grok-local-agent-kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)

**Open-source toolkit for building powerful local AI agents with MCP support, multi-LLM routing, and developer tools. Run agents offline-first. Built autonomously by Grok.**

## ✨ Features

- **Multi-LLM Support**: Ollama, LM Studio (OpenAI compatible), and more via custom providers
- **Advanced Tool System**: Web search, file ops, shell execution, MCP integration stubs
- **Autonomous Agents**: Tool-calling loops, reasoning, self-reflection, error recovery
- **CLI & SDK**: Easy command-line and Python library usage
- **MCP Ready**: Protocol support for advanced agent orchestration
- **Extensible**: Easy to add custom tools and models
- **CI/CD**: Automated testing with GitHub Actions

## 🚀 Quickstart

1. Install Ollama: https://ollama.com
2. Pull a model: `ollama pull llama3.2`
3. Install the kit:
   ```bash
   pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
   ```
4. Run:
   ```bash
   grok-agent chat "Plan a local AI agent project for 10k GitHub stars"
   ```

For LM Studio:
```bash
grok-agent chat "Your prompt" --provider lmstudio --base-url http://localhost:1234/v1
```

## 📋 Installation

```bash
pip install grok-local-agent-kit
```

Or from source for development.

## 📖 Full Documentation

- [Agent API](grok_local_agent_kit/agent.py)
- [Examples](examples/)
- [Roadmap](ROADMAP.md)

## 🛠️ Project Structure

```
.
├── grok_local_agent_kit/  # Core package
│   ├── __init__.py
│   ├── agent.py           # Main Agent class
│   ├── cli.py             # Command line interface
│   ├── tools.py           # Tool definitions
│   └── run_agent.py
├── examples/              # Ready-to-use agents
├── .github/workflows/     # CI/CD
├── pyproject.toml
├── LICENSE
├── README.md
└── ROADMAP.md
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📈 Roadmap

See [ROADMAP.md](ROADMAP.md) for v0.3+ features like advanced MCP, multi-agent orchestration, vision support.

**Star the repo ⭐ if you believe in local AI sovereignty! Built with ❤️ by Grok & community.**

## License
MIT - Free to use, modify, and distribute.