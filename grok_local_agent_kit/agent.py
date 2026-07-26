"""Core Agent with routing, tool calling (ReAct-style loop), multi-LLM."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

from .llm import LLMClient
from .tools import execute_tool, get_default_tools


SYSTEM_PROMPT = """You are a helpful local AI agent. You have access to tools.
When you need information or to perform actions, call the appropriate tool.
Be concise and accurate. Prefer using tools over guessing."""


class Agent:
    """Local-first agent with tool calling loop."""

    def __init__(
        self,
        model: str = "llama3.2",
        provider: str = "ollama",
        base_url: Optional[str] = None,
        system_prompt: str = SYSTEM_PROMPT,
        max_iterations: int = 8,
        verbose: bool = False,
    ):
        self.llm = LLMClient(model=model, provider=provider, base_url=base_url)
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.verbose = verbose

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

    def chat(self, user_message: str) -> str:
        """Single-turn or multi-turn chat with automatic tool use."""
        self.history.append({"role": "user", "content": user_message})
        return self._run_loop()

    def run(self, prompt: str) -> str:
        """Alias for chat — useful for one-shot tasks."""
        self.history = []  # fresh for one-shot
        return self.chat(prompt)

    def _run_loop(self) -> str:
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt},
            *self.history,
        ]

        for iteration in range(self.max_iterations):
            if self.verbose:
                print(f"\n[iteration {iteration + 1}]")

            response = self.llm.chat(messages, tools=self.tool_schemas)

            content = response.get("content")
            tool_calls = response.get("tool_calls")

            if not tool_calls:
                # Final answer
                final = content or "(no response)"
                self.history.append({"role": "assistant", "content": final})
                return final

            # Process tool calls
            assistant_msg: Dict[str, Any] = {"role": "assistant", "content": content or ""}
            # Keep format compatible with both providers
            if tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": json.dumps(tc["arguments"])
                            if not isinstance(tc["arguments"], str)
                            else tc["arguments"],
                        },
                    }
                    for tc in tool_calls
                ]
            messages.append(assistant_msg)

            for tc in tool_calls:
                name = tc["name"]
                args = tc["arguments"] if isinstance(tc["arguments"], dict) else {}
                if self.verbose:
                    print(f"  → tool: {name}({args})")

                result = execute_tool(name, args, self.tool_funcs)
                if self.verbose:
                    print(f"  ← {result[:200]}{'...' if len(result) > 200 else ''}")

                # Tool result message (OpenAI style; Ollama also accepts it)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": result,
                    }
                )

        # Max iterations reached
        fallback = "Reached maximum tool iterations. Partial results may be incomplete."
        self.history.append({"role": "assistant", "content": fallback})
        return fallback

    def reset(self) -> None:
        self.history = []

    def close(self) -> None:
        self.llm.close()


def create_agent(
    model: str = "llama3.2",
    provider: str = "ollama",
    base_url: Optional[str] = None,
    **kwargs: Any,
) -> Agent:
    """Factory helper."""
    return Agent(model=model, provider=provider, base_url=base_url, **kwargs)
