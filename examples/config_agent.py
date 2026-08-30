#!/usr/bin/env python3
"""Show how grok-agent.toml / env config is loaded.

Usage:
  python examples/config_agent.py
"""

from __future__ import annotations

from grok_local_agent_kit import load_config, write_example_config, __version__


def main() -> None:
    path = write_example_config("grok-agent.toml")
    cfg = load_config(path)
    print(f"config demo v{__version__}")
    print(f"wrote: {path}")
    print(f"model={cfg.model} provider={cfg.provider} router={cfg.use_router}")
    print("kwargs:", cfg.to_agent_kwargs())


if __name__ == "__main__":
    main()
