"""Core Agent with routing, tool calling (ReAct-style loop), multi-LLM."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .llm import LLMClient
from .tools import execute_tool, get_default_tools


SYSTEM_PROMPT = """You are a helpful local AI agent running entirely on the user's machine.
You have access to tools. When you need information or to perform actions, call the appropriate tool.
Be concise, accurate, and prefer using tools over guessing.
Never invent file contents, search results, or HTTP responses — always call the tool.
When a task is complete, give a clear final answer without unnecessary tool calls.
If a tool fails, explain the error briefly and try an alternative when possible.
Prefer small, focused tool calls. You can call multiple tools in sequence across turns.
For file operations stay inside the current workspace. For code, prefer execute_python over shell when safe.
Use http_get for simple page fetches and web_search for discovery.
Use get_system_info when you need OS / Python / cwd context."""

# Default max characters of a tool result kept in the conversation context
DEFAULT_TOOL_RESULT_MAX_CHARS = 6000
HISTORY_VERSION = "0.8.4"


class Agent:
    """Local-first agent with tool calling loop (ReAct-style)."""

    def __init__(
        self,
        model: str = "llama3.2",
        provider: str = "ollama",
        base_url: Optional[str] = None,
        system_prompt: str = SYSTEM_PROMPT,
        max_iterations: int = 12,
        verbose: bool = False,
        temperature: float = 0.3,
        stream: bool = False,
        tool_result_max_chars: int = DEFAULT_TOOL_RESULT_MAX_CHARS,
    ):
        self.llm = LLMClient(
            model=model, provider=provider, base_url=base_url, temperature=temperature
        )
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.stream = stream
        self.tool_result_max_chars = max(500, tool_result_max_chars)

        self.tool_schemas, self.tool_funcs = get_default_tools()
        self.history: List[Dict[str, Any]] = []

    def register_tool(
        self,
        name: str,
        func: Callable[..., str],
        description: str,
        parameters: Dict[str, Any],
    ) -> None:
        """Register a custom tool at runtime."""
        self.tool_funcs[name] = func
        self.tool_schemas.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            }
        )

    def register_tools(self, tools: List[Dict[str, Any]]) -> None:
        """
        Register multiple tools at once.
        Each item: {"name": str, "func": callable, "description": str, "parameters": dict}
        """
        for t in tools:
            self.register_tool(
                name=t["name"],
                func=t["func"],
                description=t.get("description", ""),
                parameters=t.get("parameters", {"type": "object", "properties": {}}),
            )

    def chat(self, user_message: str) -> str:
        """Single-turn or multi-turn chat with automatic tool use."""
        self.history.append({"role": "user", "content": user_message})
        return self._run_loop()

    def run(self, prompt: str) -> str:
        """One-shot task (fresh history)."""
        self.history = []
        return self.chat(prompt)

    def _truncate_tool_result(self, result: str) -> str:
        if len(result) <= self.tool_result_max_chars:
            return result
        return (
            result[: self.tool_result_max_chars]
            + f"\n\n... [truncated, original length {len(result)} chars]"
        )

    def _parse_args(self, raw_args: Any) -> Dict[str, Any]:
        if isinstance(raw_args, dict):
            return raw_args
        if isinstance(raw_args, str):
            raw = raw_args.strip()
            if not raw:
                return {}
            try:
                parsed = json.loads(raw)
                return parsed if isinstance(parsed, dict) else {"raw": raw}
            except json.JSONDecodeError:
                return {"raw": raw}
        return {}

    def _run_loop(self) -> str:
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt},
            *self.history,
        ]

        for iteration in range(self.max_iterations):
            if self.verbose:
                print(f"\n[iteration {iteration + 1}/{self.max_iterations}]")

            # Non-streaming call first so we can reliably detect tool_calls.
            response = self.llm.chat(messages, tools=self.tool_schemas)

            content = response.get("content")
            tool_calls = response.get("tool_calls")

            if not tool_calls:
                # Final answer path. Optionally re-stream for live UX when stream=True.
                if self.stream:
                    final_parts: List[str] = []
                    stream_resp = self.llm.stream_chat(messages, tools=None)
                    try:
                        while True:
                            chunk = next(stream_resp)
                            if isinstance(chunk, str) and chunk:
                                final_parts.append(chunk)
                                if self.verbose:
                                    print(chunk, end="", flush=True)
                    except StopIteration as stop:
                        ret = stop.value if stop.value is not None else {}
                        if isinstance(ret, dict) and ret.get("content"):
                            final = ret["content"].strip()
                        else:
                            final = ("".join(final_parts) or content or "(no response)").strip()
                    if self.verbose and final_parts:
                        print()  # newline after live tokens
                else:
                    final = (content or "(no response)").strip()

                self.history.append({"role": "assistant", "content": final})
                return final

            # Assistant message compatible with Ollama & OpenAI-compatible
            assistant_msg: Dict[str, Any] = {
                "role": "assistant",
                "content": content or "",
            }
            assistant_msg["tool_calls"] = [
                {
                    "id": tc.get("id") or f"call_{i}",
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["arguments"])
                        if not isinstance(tc["arguments"], str)
                        else tc["arguments"],
                    },
                }
                for i, tc in enumerate(tool_calls)
            ]
            messages.append(assistant_msg)

            for tc in tool_calls:
                name = tc.get("name") or ""
                args = self._parse_args(tc.get("arguments", {}))

                if self.verbose:
                    print(f"  → tool: {name}({args})")

                result = execute_tool(name, args, self.tool_funcs)
                result = self._truncate_tool_result(result)

                if self.verbose:
                    preview = result[:300] + ("..." if len(result) > 300 else "")
                    print(f"  ← {preview}")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.get("id") or f"call_{name}",
                        "content": result,
                    }
                )

        fallback = (
            "Reached maximum tool iterations. "
            "Partial results may be incomplete — try a more focused prompt."
        )
        self.history.append({"role": "assistant", "content": fallback})
        return fallback

    def reset(self) -> None:
        """Clear conversation history."""
        self.history = []

    def get_history(self) -> list:
        """Return a shallow copy of the conversation history."""
        return list(self.history)

    def list_registered_tools(self) -> List[str]:
        """Return the names of all currently registered tools."""
        return sorted(self.tool_funcs.keys())

    def close(self) -> None:
        self.llm.close()

    def save_history(self, path: str = "agent_history.json") -> str:
        """Persist conversation history to a JSON file (cwd-safe)."""
        try:
            p = Path(path).expanduser().resolve()
            cwd = Path.cwd().resolve()
            p.relative_to(cwd)  # safety
            data = {"history": self.history, "version": HISTORY_VERSION}
            p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            return f"Saved {len(self.history)} messages to {p}"
        except Exception as e:
            return f"save_history error: {e}"

    def load_history(self, path: str = "agent_history.json") -> str:
        """Load conversation history from a JSON file (cwd-safe)."""
        try:
            p = Path(path).expanduser().resolve()
            cwd = Path.cwd().resolve()
            p.relative_to(cwd)
            data = json.loads(p.read_text(encoding="utf-8"))
            self.history = data.get("history", [])
            return f"Loaded {len(self.history)} messages from {p}"
        except Exception as e:
            return f"load_history error: {e}"


def create_agent(
    model: Optional[str] = None,
    provider: Optional[str] = None,
    base_url: Optional[str] = None,
    **kwargs: Any,
) -> Agent:
    """
    Factory helper. Accepts provider aliases: ollama | lmstudio | openai.

    Environment variables (used as defaults when args omitted):
      GROK_AGENT_MODEL, GROK_AGENT_PROVIDER, GROK_AGENT_BASE_URL
    """
    model = model or os.environ.get("GROK_AGENT_MODEL", "llama3.2")
    provider = (provider or os.environ.get("GROK_AGENT_PROVIDER", "ollama")).lower().strip()
    base_url = base_url or os.environ.get("GROK_AGENT_BASE_URL")

    if provider == "lmstudio":
        provider = "openai"
        base_url = base_url or "http://localhost:1234/v1"
    return Agent(model=model, provider=provider, base_url=base_url, **kwargs)
