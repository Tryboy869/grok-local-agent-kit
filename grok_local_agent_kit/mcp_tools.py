"""MCP resource tool + memory tools registered into the default toolkit."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from .memory import forget, recall, remember


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

MEMORY_SPECS = [
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Persist a short note in local agent memory (.grok/memory).",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}, "tags": {"type": "string"}},
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": "Search local agent memory notes.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "forget",
            "description": "Delete local memory notes matching a query.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]

MEMORY_FUNCS = {"remember": remember, "recall": recall, "forget": forget}


def extend_default_tools(
    schemas: List[Dict[str, Any]], funcs: Dict[str, Callable[..., str]]
) -> tuple[List[Dict[str, Any]], Dict[str, Callable[..., str]]]:
    funcs = dict(funcs)
    schemas = list(schemas)
    if "mcp_read_resource" not in funcs:
        funcs["mcp_read_resource"] = mcp_read_resource
        schemas.append(MCP_READ_SPEC)
    for spec in MEMORY_SPECS:
        name = spec["function"]["name"]
        if name not in funcs:
            funcs[name] = MEMORY_FUNCS[name]
            schemas.append(spec)
    return schemas, funcs
