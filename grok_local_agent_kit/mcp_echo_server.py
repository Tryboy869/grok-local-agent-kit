"""Tiny MCP stdio echo server used by tests and as a config example.

Speaks newline-delimited JSON-RPC 2.0 on stdin/stdout.
Tools: echo, add. Resource: echo://about
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict


def _respond(msg_id: Any, result: Any) -> None:
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}) + "\n")
    sys.stdout.flush()


def _error(msg_id: Any, message: str, code: int = -32000) -> None:
    sys.stdout.write(
        json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}) + "\n"
    )
    sys.stdout.flush()


def main() -> None:
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            req = json.loads(raw)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        msg_id = req.get("id")
        params = req.get("params") or {}
        if method and method.startswith("notifications/"):
            continue
        if method == "initialize":
            _respond(
                msg_id,
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}, "resources": {}},
                    "serverInfo": {"name": "grok-echo", "version": "0.9.1"},
                },
            )
        elif method == "tools/list":
            _respond(
                msg_id,
                {
                    "tools": [
                        {
                            "name": "echo",
                            "description": "Echo back a message",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"message": {"type": "string"}},
                                "required": ["message"],
                            },
                        },
                        {
                            "name": "add",
                            "description": "Add two numbers",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                                "required": ["a", "b"],
                            },
                        },
                    ]
                },
            )
        elif method == "resources/list":
            _respond(
                msg_id,
                {
                    "resources": [
                        {"uri": "echo://about", "name": "about", "mimeType": "text/plain"}
                    ]
                },
            )
        elif method == "resources/read":
            uri = params.get("uri")
            if uri == "echo://about":
                _respond(
                    msg_id,
                    {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "text/plain",
                                "text": "grok-echo MCP server v0.9.1",
                            }
                        ]
                    },
                )
            else:
                _error(msg_id, f"unknown resource: {uri}")
        elif method == "tools/call":
            name = params.get("name")
            args: Dict[str, Any] = params.get("arguments") or {}
            if name == "echo":
                text = str(args.get("message", ""))
                _respond(msg_id, {"content": [{"type": "text", "text": text}]})
            elif name == "add":
                try:
                    total = float(args.get("a", 0)) + float(args.get("b", 0))
                except (TypeError, ValueError) as e:
                    _error(msg_id, f"bad args: {e}")
                    continue
                _respond(msg_id, {"content": [{"type": "text", "text": str(total)}]})
            else:
                _error(msg_id, f"unknown tool: {name}")
        else:
            if msg_id is not None:
                _error(msg_id, f"unknown method: {method}", code=-32601)


if __name__ == "__main__":
    main()
