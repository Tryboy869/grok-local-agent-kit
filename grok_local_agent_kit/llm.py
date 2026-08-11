"""Multi-LLM client: Ollama (native) + any OpenAI-compatible endpoint (LM Studio, vLLM, etc.)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import httpx

try:
    import ollama
except ImportError:  # pragma: no cover
    ollama = None  # type: ignore


class LLMClient:
    """Unified interface for local LLMs (Ollama + OpenAI-compatible)."""

    def __init__(
        self,
        model: str = "llama3.2",
        provider: str = "ollama",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.3,
        timeout: float = 120.0,
    ):
        self.model = model
        self.provider = provider.lower().strip()
        self.temperature = temperature
        self.timeout = timeout

        if self.provider in {"ollama"}:
            self.base_url = (base_url or "http://localhost:11434").rstrip("/")
            self._client: Optional[httpx.Client] = None
        else:
            # openai / lmstudio / vllm / any OpenAI-compatible server
            default = "http://localhost:1234/v1"
            self.base_url = (base_url or default).rstrip("/")
            self.api_key = api_key or "lm-studio"
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=timeout,
            )

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
    ) -> Dict[str, Any]:
        """
        Normalized response:
        {
          "content": str | None,
          "tool_calls": list[{"id", "name", "arguments"}] | None,
          "raw": original
        }
        """
        if self.provider == "ollama":
            return self._chat_ollama(messages, tools)
        return self._chat_openai_compat(messages, tools, tool_choice)

    def _chat_ollama(
        self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        if ollama is None:
            return {
                "content": (
                    "[LLM error] ollama package not installed. "
                    "Run: pip install ollama"
                ),
                "tool_calls": None,
                "raw": None,
            }

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "options": {"temperature": self.temperature},
        }
        if tools:
            kwargs["tools"] = tools

        try:
            resp = ollama.chat(**kwargs)
        except Exception as e:
            return {
                "content": (
                    f"[LLM error] {e}. "
                    "Is Ollama running? Try: ollama serve && ollama pull {self.model}"
                ),
                "tool_calls": None,
                "raw": None,
            }

        msg = resp.get("message", {}) or {}
        content = msg.get("content") or None
        tool_calls = None

        if msg.get("tool_calls"):
            tool_calls = []
            for tc in msg["tool_calls"]:
                fn = tc.get("function", {}) or {}
                args = fn.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args) if args.strip() else {}
                    except json.JSONDecodeError:
                        args = {"raw": args}
                tool_calls.append(
                    {
                        "id": tc.get("id") or f"call_{len(tool_calls)}",
                        "name": fn.get("name", ""),
                        "arguments": args if isinstance(args, dict) else {"raw": args},
                    }
                )

        return {"content": content, "tool_calls": tool_calls, "raw": resp}

    def _chat_openai_compat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]],
        tool_choice: str,
    ) -> Dict[str, Any]:
        assert self._client is not None
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice

        try:
            r = self._client.post("/chat/completions", json=payload)
            r.raise_for_status()
            data = r.json()
        except httpx.ConnectError:
            return {
                "content": (
                    f"[LLM error] Cannot reach {self.base_url}. "
                    "Is LM Studio / OpenAI-compatible server running?"
                ),
                "tool_calls": None,
                "raw": None,
            }
        except Exception as e:
            return {"content": f"[LLM error] {e}", "tool_calls": None, "raw": None}

        choice = (data.get("choices") or [{}])[0].get("message") or {}
        content = choice.get("content")
        tool_calls = None

        if choice.get("tool_calls"):
            tool_calls = []
            for tc in choice["tool_calls"]:
                fn = tc.get("function") or {}
                args = fn.get("arguments", "{}")
                if isinstance(args, str):
                    try:
                        args = json.loads(args) if args.strip() else {}
                    except json.JSONDecodeError:
                        args = {"raw": args}
                tool_calls.append(
                    {
                        "id": tc.get("id") or f"call_{len(tool_calls)}",
                        "name": fn.get("name", ""),
                        "arguments": args if isinstance(args, dict) else {"raw": args},
                    }
                )

        return {"content": content, "tool_calls": tool_calls, "raw": data}

    def stream_chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Yield content chunks when the model produces a final answer without tools.
        Falls back to a single full response if streaming is unavailable.
        When tools are present, streaming is skipped (tool-calling is more reliable non-stream).
        """
        if tools:
            yield from []
            return self.chat(messages, tools=tools)

        if self.provider == "ollama":
            if ollama is None:
                yield "[LLM error] ollama package not installed."
                return {"content": None, "tool_calls": None, "raw": None}
            try:
                stream = ollama.chat(
                    model=self.model,
                    messages=messages,
                    options={"temperature": self.temperature},
                    stream=True,
                )
                full = ""
                for chunk in stream:
                    msg = chunk.get("message", {}) or {}
                    delta = msg.get("content") or ""
                    if delta:
                        full += delta
                        yield delta
                return {"content": full, "tool_calls": None, "raw": None}
            except Exception as e:
                yield f"[LLM error] {e}"
                return {"content": None, "tool_calls": None, "raw": None}

        # OpenAI-compatible streaming
        assert self._client is not None
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": True,
        }
        try:
            with self._client.stream("POST", "/chat/completions", json=payload) as r:
                r.raise_for_status()
                full = ""
                for line in r.iter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        obj = json.loads(data)
                        delta = (obj.get("choices") or [{}])[0].get("delta") or {}
                        piece = delta.get("content") or ""
                        if piece:
                            full += piece
                            yield piece
                    except Exception:
                        continue
                return {"content": full, "tool_calls": None, "raw": None}
        except Exception as e:
            yield f"[LLM error] {e}"
            return {"content": None, "tool_calls": None, "raw": None}

    def ping(self) -> str:
        """Lightweight connectivity check."""
        try:
            if self.provider == "ollama":
                if ollama is None:
                    return "ollama package missing"
                models = ollama.list()
                names = [
                    m.get("name") or m.get("model", "?")
                    for m in models.get("models", [])
                ]
                return f"ok — models: {', '.join(names[:8]) or '(none)'}"
            assert self._client is not None
            r = self._client.get("/models")
            if r.status_code >= 400:
                return f"HTTP {r.status_code}"
            data = r.json()
            ids = [m.get("id", "?") for m in data.get("data", [])]
            return f"ok — models: {', '.join(ids[:8]) or '(none)'}"
        except Exception as e:
            return f"unreachable: {e}"

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
