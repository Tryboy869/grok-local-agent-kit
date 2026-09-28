#!/usr/bin/env python3
"""Discover local Ollama / LM Studio models (no chat required)."""

from grok_local_agent_kit.catalog import demo_catalog

if __name__ == "__main__":
    print(demo_catalog())
