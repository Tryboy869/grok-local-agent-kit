# 🚀 Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![PyPI version](https://img.shields.io/pypi/v/grok-local-agent-kit.svg)](https://pypi.org/project/grok-local-agent-kit/)

**Autonomous local AI agents toolkit powered by Grok. Supports Ollama, MCP, multi-agent orchestration, tools, and offline-first execution. Built to empower developers with privacy-focused AI agents.**

## ✨ Key Features

- **Local LLM Support**: Ollama, LM Studio, vLLM, HuggingFace
- **MCP Protocol**: Model Context Protocol for tool calling and agent communication
- **Agent Framework**: Single, multi-agent, hierarchical, swarms
- **Tools**: File I/O, web search, code execution, shell, custom tools
- **CLI & Python API**: Easy scripting and integration
- **Extensible Skills**: .grok/skills compatible
- **CI/CD**: GitHub Actions for testing and publishing

## 🚀 Quickstart

```bash
# Install
pip install grok-local-agent-kit

# Run CLI
grok-agent --model ollama/llama3.2 "Plan and implement a simple todo app"

# Python example
from grok_local_agent_kit.agent import LocalAgent

agent = LocalAgent(model="llama3.2")
result = agent.run("Hello, create a function to sum numbers.")
print(result)
```

**Prerequisites**: Install [Ollama](https://ollama.com) and pull a model: `ollama pull llama3.2`

## 📁 Structure

```
grok-local-agent-kit/
├── grok_local_agent_kit/     # Core package
├── examples/                 # Usage demos
├── .github/workflows/        # CI
├── README.md, LICENSE, etc.
```

## 📖 Documentation

- [Agent Guide](docs/agent.md) (coming soon)
- [MCP Setup](docs/mcp.md)
- Full [ROADMAP.md](ROADMAP.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Stars and PRs highly appreciated!

## License
MIT © Tryboy869 & Grok

---
*Autonomously initialized and enhanced by Grok. Goal: 10k stars in 3 months. Join the movement!*