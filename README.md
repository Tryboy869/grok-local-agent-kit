# 🚀 Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![PyPI](https://img.shields.io/pypi/v/grok-local-agent-kit.svg)](https://pypi.org/project/grok-local-agent-kit/)
[![Downloads](https://img.shields.io/pypi/dm/grok-local-agent-kit.svg)](https://pypi.org/project/grok-local-agent-kit/)

**The ultimate open-source toolkit for running powerful, autonomous AI agents locally.** Powered by Ollama, MCP protocol support, tool calling, multi-agent systems, and more. No cloud dependency — full offline capability. Built autonomously by Grok to democratize agentic AI.

## ✨ Features

- **Local-First LLMs**: Seamless integration with Ollama, vLLM, LM Studio.
- **MCP Support**: Standardized Multi-Context Protocol for rich agent interactions.
- **Advanced Tools**: Web search, code execution, file operations, browser automation, custom skills.
- **CLI & Python SDK**: Intuitive command-line and programmable interface.
- **Multi-Agent Orchestration**: Swarm intelligence, hierarchical agents, collaboration.
- **Autonomous Mode**: Goal-driven agents that plan, execute, and iterate.
- **Extensible**: Plugin system for skills, tools, and custom models.
- **CI/CD Ready**: GitHub Actions for testing and deployment.

## 🚀 Quickstart

1. Install:
   ```bash
   pip install grok-local-agent-kit ollama duckduckgo-search
   ```

2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```

3. Run CLI:
   ```bash
   grok-agent chat "Help me build a simple web scraper"
   ```

4. Python example:
   ```python
   from grok_local_agent_kit import create_agent

   agent = create_agent('llama3.2')
   result = agent.run("Explain quantum computing simply")
   print(result)
   ```

## 📖 Documentation

- [Installation](./docs/install.md)
- [Agent API](./docs/api.md)
- [Tools](./docs/tools.md)
- [MCP Guide](./docs/mcp.md)
- [Examples](./examples/)

## 🛣️ Roadmap

See [ROADMAP.md](ROADMAP.md) for details:
- v0.4: Advanced multi-agent
- v1.0: Full MCP server, vision support
- v2.0: Distributed agents, marketplace

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Stars and PRs welcome!

## License
MIT - see [LICENSE](LICENSE)

⭐ **Star this repo to help us reach 10k stars and make local agents mainstream!**