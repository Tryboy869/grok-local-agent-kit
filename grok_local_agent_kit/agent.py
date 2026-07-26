"""
Core Agent implementation with Ollama, tool calling and simple ReAct loop.
"""

from __future__ import annotations

import json
import re
from typing import Any, Callable, Dict, List, Optional

import ollama
from rich.console import Console

from .tools import DEFAULT_TOOLS, Tool

console = Console()


class Agent:
    """A local autonomous agent that can use tools via Ollama."""

    def __init__(
        self,
        model: str = "llama3.2",
        system_prompt: Optional[str] = None,
        tools: Optional[List[Tool]] = None,
        max_iterations: int = 6,
        verbose: bool = True,
    ):
        self.model = model
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.tools: Dict[str, Tool] = {}
        self.history: List[Dict[str, str]] = []

        default_system = (
            "You are a helpful autonomous local AI agent. "
            "You have access to tools. When you need a tool, reply ONLY with a JSON block:\n"
            '{"tool": "tool_name", "args": {"arg1": "value"}}\n'
            "Otherwise reply with a normal helpful answer. "
            "Be concise and accurate."
        )
        self.system_prompt = system_prompt or default_system

        # Register default tools
        for t in tools or DEFAULT_TOOLS:
            self.register_tool(t)

    def register_tool(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def _tool_descriptions(self) -> str:
        lines = []
        for name, tool in self.tools.items():
            lines.append(f"- {name}: {tool.description}")
            if tool.parameters:
                lines.append(f"  parameters: {json.dumps(tool.parameters)}")
        return "\n".join(lines)

    def _build_messages(self, user_prompt: str) -> List[Dict[str, str]]:
        tools_desc = self._tool_descriptions()
        system = (
            f"{self.system_prompt}\n\n"
            f"Available tools:\n{tools_desc}\n\n"
            "If you need a tool, output ONLY the JSON object, nothing else."
        )
        messages = [{"role": "system", "content": system}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_prompt})
        return messages

    def _parse_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        # Try to extract a JSON object that looks like a tool call
        match = re.search(r"\{[^{}]*\"tool\"[^{}]*\}", text, re.DOTALL)
        if not match:
            # also try full JSON
            match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                if isinstance(data, dict) and "tool" in data:
                    return data
            except json.JSONDecodeError:
                pass
        return None

    def run(self, prompt: str) -> str:
        """Run the agent on a prompt (single-shot or multi-step with tools)."""
        if self.verbose:
            console.print(f"[bold blue]Agent[/] thinking with model [cyan]{self.model}[/]...")

        messages = self._build_messages(prompt)
        final_answer = ""

        for iteration in range(self.max_iterations):
            try:
                response = ollama.chat(model=self.model, messages=messages)
                content = response["message"]["content"].strip()
            except Exception as e:
                return f"Error talking to Ollama: {e}. Is Ollama running and is the model pulled?"

            if self.verbose:
                console.print(f"[dim]Iteration {iteration + 1}:[/] {content[:200]}{'...' if len(content) > 200 else ''}")

            tool_call = self._parse_tool_call(content)

            if tool_call is None:
                # No tool → final answer
                final_answer = content
                break

            tool_name = tool_call.get("tool")
            args = tool_call.get("args", {}) or {}

            if tool_name not in self.tools:
                observation = f"Unknown tool: {tool_name}. Available: {list(self.tools.keys())}"
            else:
                try:
                    observation = str(self.tools[tool_name].func(**args))
                except Exception as e:
                    observation = f"Tool error: {e}"

            if self.verbose:
                console.print(f"[yellow]Tool {tool_name} →[/] {observation[:300]}")

            # Feed observation back
            messages.append({"role": "assistant", "content": content})
            messages.append(
                {
                    "role": "user",
                    "content": f"Tool result:\n{observation}\n\nContinue or give the final answer.",
                }
            )
        else:
            final_answer = content or "Max iterations reached."

        # Update history (keep it light)
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": final_answer})
        if len(self.history) > 20:
            self.history = self.history[-20:]

        return final_answer

    def chat(self, prompt: str) -> str:
        """Alias for run (compatible with examples)."""
        return self.run(prompt)

    def reset(self) -> None:
        self.history.clear()


def create_agent(
    model: str = "llama3.2",
    system_prompt: Optional[str] = None,
    verbose: bool = True,
    **kwargs: Any,
) -> Agent:
    """Factory helper."""
    return Agent(model=model, system_prompt=system_prompt, verbose=verbose, **kwargs)
