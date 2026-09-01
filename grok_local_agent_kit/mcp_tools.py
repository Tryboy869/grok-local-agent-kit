"""MCP resource tool + memory tools registered into the default toolkit."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from .memory import forget, recall, remember
from .vector_memory import vrecall, vremember


def mcp_read_resource(uri: str) -> str:
    from .mcp import get_manager

    return get_manager().read_resource(uri)


def mcp_list_prompts() -> str:
    from .mcp import get_manager

    return get_manager().list_prompts()


def mcp_get_prompt(name: str, arguments: str = "") -> str:
    from .mcp import get_manager
    import json

    args: Dict[str, Any] = {}
    raw = (arguments or "").strip()
    if raw:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                args = parsed
        except json.JSONDecodeError:
            args = {"raw": raw}
    return get_manager().get_prompt(name, args)


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

MCP_PROMPT_SPECS = [
    {
        "type": "function",
        "function": {
            "name": "mcp_list_prompts",
            "description": "List prompts advertised by configured MCP servers.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mcp_get_prompt",
            "description": "Fetch an MCP prompt by name (optional JSON arguments).",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "arguments": {"type": "string", "description": "JSON object as string"},
                },
                "required": ["name"],
            },
        },
    },
]

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
    {
        "type": "function",
        "function": {
            "name": "vremember",
            "description": "Store a note in SQLite vector memory (hashed bag-of-words).",
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
            "name": "vrecall",
            "description": "Semantic-ish search over SQLite vector memory.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
                "required": ["query"],
            },
        },
    },
]

MEMORY_FUNCS = {
    "remember": remember,
    "recall": recall,
    "forget": forget,
    "vremember": vremember,
    "vrecall": vrecall,
}


def extend_default_tools(
    schemas: List[Dict[str, Any]], funcs: Dict[str, Callable[..., str]]
) -> tuple[List[Dict[str, Any]], Dict[str, Callable[..., str]]]:
    funcs = dict(funcs)
    schemas = list(schemas)
    if "mcp_read_resource" not in funcs:
        funcs["mcp_read_resource"] = mcp_read_resource
        schemas.append(MCP_READ_SPEC)
    if "mcp_list_prompts" not in funcs:
        funcs["mcp_list_prompts"] = mcp_list_prompts
        funcs["mcp_get_prompt"] = mcp_get_prompt
        schemas.extend(MCP_PROMPT_SPECS)
    for spec in MEMORY_SPECS:
        name = spec["function"]["name"]
        if name not in funcs:
            funcs[name] = MEMORY_FUNCS[name]
            schemas.append(spec)
    return schemas, funcs
