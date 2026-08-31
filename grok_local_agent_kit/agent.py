"""Core Agent with routing, tool calling (ReAct-style loop), multi-LLM, hooks."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .hooks import HookBus
from .llm import LLMClient
from .mcp_tools import extend_default_tools
from .session import HISTORY_VERSION, list_sessions, load_session, save_session
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
Use search_files to find files whose content matches a query (text search in workspace).
Use get_system_info when you need OS / Python / cwd context.
Use delete_file only when the user explicitly asks to remove a file.
Use remember / recall / forget for durable local notes.
Use mcp_read_resource to fetch MCP resource URIs after mcp_list_resources.
Discovered MCP tools may appear as mcp_<server>_<tool> after attach_mcp_tools().
Route carefully: list_files or search_files before write/read when unsure of paths; calculator for pure math; run_shell only for safe, non-destructive commands."""

DEFAULT_TOOL_RESULT_MAX_CHARS = 6000


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
        session_name: Optional[str] = None,
        attach_mcp: bool = False,
        hooks: Optional[HookBus] = None,
    ):
        self.llm = LLMClient(
            model=model, provider=provider, base_url=base_url, temperature=temperature
        )
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.stream = stream
        self.tool_result_max_chars = max(500, tool_result_max_chars)
        self.session_name = session_name or "default"
        self.hooks = hooks if hooks is not None else HookBus()
        self.last_trace: List[Dict[str, Any]] = []

        self.tool_schemas, self.tool_funcs = extend_default_tools(*get_default_tools())
        self.history: List[Dict[str, Any]] = []
        if attach_mcp:
            self.attach_mcp_tools()

    def on(self, event: str, fn: Callable[..., None]) -> Callable[..., None]:
        return self.hooks.on(event, fn)

    def register_tool(
        self,
        name: str,
        func: Callable[..., str],
        description: str,
        parameters: Dict[str, Any],
    ) -> None:
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
        for t in tools:
            self.register_tool(
                name=t["name"],
                func=t["func"],
                description=t.get("description", ""),
                parameters=t.get("parameters", {"type": "object", "properties": {}}),
            )

    def attach_mcp_tools(self) -> List[str]:
        """Discover MCP stdio tools and register them as mcp_<server>_<tool>."""
        from .mcp import get_manager

        added: List[str] = []
        for item in get_manager().discover_tools():
            qname = item["qualified_name"]
            if qname in self.tool_funcs:
                continue
            remote_name = item["name"]

            def _make(tool_name: str) -> Callable[..., str]:
                def _call(**kwargs: Any) -> str:
                    from .mcp import get_manager as _gm

                    return _gm().call_tool(tool_name, kwargs)

                return _call

            self.register_tool(
                qname,
                _make(remote_name),
                item.get("description") or f"MCP tool {remote_name}",
                item.get("parameters") or {"type": "object", "properties": {}},
            )
            added.append(qname)
        if self.verbose:
            print(f"  attached MCP tools: {added or '(none)'}")
        return added

    def load_skills(self, directory: Optional[str] = None) -> List[str]:
        """Load extra tools from .grok/skills/*.json skill manifests."""
        from .skills import load_skills

        return load_skills(self, directory)

    def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        return self._run_loop()

    def run(self, prompt: str) -> str:
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
        self.last_trace = []
        self.hooks.emit("on_start", agent=self, messages=messages)

        for iteration in range(self.max_iterations):
            if self.verbose:
                print(f"\n[iteration {iteration + 1}/{self.max_iterations}]")
            self.hooks.emit("on_iteration", agent=self, iteration=iteration)
            self.hooks.emit("before_llm", agent=self, messages=messages, iteration=iteration)

            response = self.llm.chat(messages, tools=self.tool_schemas)
            self.hooks.emit("after_llm", agent=self, response=response, iteration=iteration)

            content = response.get("content")
            tool_calls = response.get("tool_calls")

            if not tool_calls:
                if self.stream and not (content and str(content).strip()):
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
                            final = (
                                "".join(final_parts) or content or "(no response)"
                            ).strip()
                    if self.verbose and final_parts:
                        print()
                elif self.stream and content and self.verbose:
                    print(content, end="", flush=True)
                    print()
                    final = str(content).strip()
                else:
                    final = (content or "(no response)").strip()

                self.history.append({"role": "assistant", "content": final})
                self.last_trace.append({"type": "final", "text": final})
                self.hooks.emit("on_final", agent=self, text=final)
                return final

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

                self.hooks.emit("before_tool", agent=self, name=name, args=args)
                result = execute_tool(name, args, self.tool_funcs)
                result = self._truncate_tool_result(result)
                self.hooks.emit(
                    "after_tool", agent=self, name=name, args=args, result=result
                )
                self.last_trace.append(
                    {"type": "tool", "name": name, "args": args, "result": result[:500]}
                )

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
        self.last_trace.append({"type": "final", "text": fallback, "reason": "max_iterations"})
        self.hooks.emit("on_final", agent=self, text=fallback)
        return fallback

    def reset(self) -> None:
        self.history = []
        self.last_trace = []

    def get_history(self) -> list:
        return list(self.history)

    def list_registered_tools(self) -> List[str]:
        return sorted(self.tool_funcs.keys())

    def close(self) -> None:
        self.llm.close()
        try:
            from .mcp import get_manager

            get_manager().close()
        except Exception:
            pass

    def save_history(self, path: str = "agent_history.json") -> str:
        try:
            p = Path(path).expanduser().resolve()
            cwd = Path.cwd().resolve()
            p.relative_to(cwd)
            data = {"history": self.history, "version": HISTORY_VERSION}
            p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            return f"Saved {len(self.history)} messages to {p}"
        except Exception as e:
            return f"save_history error: {e}"

    def load_history(self, path: str = "agent_history.json") -> str:
        try:
            p = Path(path).expanduser().resolve()
            cwd = Path.cwd().resolve()
            p.relative_to(cwd)
            data = json.loads(p.read_text(encoding="utf-8"))
            self.history = data.get("history", [])
            return f"Loaded {len(self.history)} messages from {p}"
        except Exception as e:
            return f"load_history error: {e}"

    def save_named_session(self, name: Optional[str] = None) -> str:
        try:
            target = name or self.session_name
            self.session_name = target
            return save_session(target, self.history)
        except Exception as e:
            return f"save_session error: {e}"

    def load_named_session(self, name: str) -> str:
        try:
            data = load_session(name)
            self.history = data.get("history", [])
            self.session_name = name
            return f"Loaded session '{name}' ({len(self.history)} messages)"
        except Exception as e:
            return f"load_session error: {e}"

    def list_named_sessions(self) -> str:
        names = list_sessions()
        if not names:
            return "No named sessions in .grok/sessions/"
        return "Sessions:\n" + "\n".join(f"- {n}" for n in names)


def create_agent(
    model: Optional[str] = None,
    provider: Optional[str] = None,
    base_url: Optional[str] = None,
    **kwargs: Any,
) -> Agent:
    model = model or os.environ.get("GROK_AGENT_MODEL", "llama3.2")
    provider = (provider or os.environ.get("GROK_AGENT_PROVIDER", "ollama")).lower().strip()
    base_url = base_url or os.environ.get("GROK_AGENT_BASE_URL")

    if provider == "lmstudio":
        provider = "openai"
        base_url = base_url or "http://localhost:1234/v1"
    return Agent(model=model, provider=provider, base_url=base_url, **kwargs)
