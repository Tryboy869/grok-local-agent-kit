# Grok Local Agent Kit

[![Stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**The open-source toolkit for building autonomous local AI agents.**

Run powerful agents offline with MCP server integration, multi-LLM support (Ollama, LM Studio, etc.), reusable skills, and developer productivity tools.

Built autonomously by Grok (xAI) to show transparent open-source AI development.

## ✨ Features

- 🚀 **Offline-first** agents powered by local LLMs
- 🔌 Native **MCP Server** support for secure tool calling
- 🛠 **Curated agent skills** library (code gen, research, automation)
- 🔀 Intelligent multi-LLM routing & fallback
- 📦 CLI, Python SDK, and future JS support
- 🧠 Persistent memory & long-term planning
- 🌐 Browser & system tool integrations

## Quick Start

1. Install:
```bash
pip install grok-local-agent-kit
```

2. Run your first agent:
```python
from grok_local_agent_kit.agent import Agent

agent = Agent(llm="ollama/llama3.1")
response = agent.run("Create a simple web scraper and save results")
print(response)
```

## Documentation

Full docs in `/docs`.

## Contributing
Welcoming PRs! See [CONTRIBUTING.md](CONTRIBUTING.md)

⭐ Star if you find it useful!

Built with ❤️ by Grok.