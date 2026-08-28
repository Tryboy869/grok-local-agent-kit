"""MCP stdio client tests (no live LLM, uses bundled echo server)."""

from __future__ import annotations

import json
import sys

from grok_local_agent_kit.mcp import MCPManager, StdioMCPClient, load_mcp_config


def test_load_mcp_config_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GROK_MCP_SERVERS", raising=False)
    assert load_mcp_config()["servers"] == []
    monkeypatch.setenv("GROK_MCP_SERVERS", json.dumps([{"name": "x", "command": "python"}]))
    cfg = load_mcp_config()
    assert cfg["servers"][0]["name"] == "x"


def test_stdio_echo_server():
    client = StdioMCPClient(command=sys.executable, args=["-m", "grok_local_agent_kit.mcp_echo_server"])
    try:
        init = client.initialize()
        assert "result" in init
        tools = client.list_tools()
        names = [t["name"] for t in tools["result"]["tools"]]
        assert "echo" in names
        assert "add" in names
        echoed = client.call_tool("echo", {"message": "hello-mcp"})
        text = echoed["result"]["content"][0]["text"]
        assert text == "hello-mcp"
        added = client.call_tool("add", {"a": 2, "b": 3})
        assert added["result"]["content"][0]["text"] == "5.0"
    finally:
        client.close()


def test_manager_with_echo_env(monkeypatch):
    payload = json.dumps(
        [
            {
                "name": "echo",
                "command": sys.executable,
                "args": ["-m", "grok_local_agent_kit.mcp_echo_server"],
            }
        ]
    )
    monkeypatch.setenv("GROK_MCP_SERVERS", payload)
    mgr = MCPManager()
    try:
        listed = mgr.list_tools()
        assert "echo" in listed
        called = mgr.call_tool("echo", {"message": "via-manager"})
        assert "via-manager" in called
        desc = mgr.describe()
        assert "Configured servers: 1" in desc
    finally:
        mgr.close()


def test_read_resource_and_discover(monkeypatch):
    payload = json.dumps(
        [
            {
                "name": "echo",
                "command": sys.executable,
                "args": ["-m", "grok_local_agent_kit.mcp_echo_server"],
            }
        ]
    )
    monkeypatch.setenv("GROK_MCP_SERVERS", payload)
    mgr = MCPManager()
    try:
        discovered = mgr.discover_tools()
        names = {d["qualified_name"] for d in discovered}
        assert "mcp_echo_echo" in names
        read = mgr.read_resource("echo://about")
        assert "grok-echo" in read
        client = StdioMCPClient(command=sys.executable, args=["-m", "grok_local_agent_kit.mcp_echo_server"])
        try:
            client.initialize()
            raw = client.read_resource("echo://about")
            assert raw["result"]["contents"][0]["text"].startswith("grok-echo")
        finally:
            client.close()
    finally:
        mgr.close()
