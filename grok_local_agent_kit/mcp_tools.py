"""MCP resource tool registered into the default toolkit."""

from __future__ import annotations

from typing import Any, Callable, Dict, List


def mcp_read_resource(uri: str) -> str:
    from .mcp import get_manager

    return get_manager().read_resource(uri)


MCP_READ_SPEC = {
    "type": "function",
    "function": {
        "name": "mcp_read_resource",
        "description": "Read an MCP resource by URI (resources/read).",
        "parameters": {
            "type": "object",
            "properties": {"uri": {"type": "string"}},
            "required": ["uri"],
        },
    },
}


def extend_default_tools(
    schemas: List[Dict[str, Any]], funcs: Dict[str, Callable[..., str]]
) -> tuple[List[Dict[str, Any]], Dict[str, Callable[..., str]]]:
    if "mcp_read_resource" not in funcs:
        funcs = dict(funcs)
        funcs["mcp_read_resource"] = mcp_read_resource
        schemas = list(schemas) + [MCP_READ_SPEC]
    return schemas, funcs
