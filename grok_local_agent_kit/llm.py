"""Multi-LLM client: Ollama (native) + any OpenAI-compatible endpoint (LM Studio, vLLM, etc.)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import httpx
import ollama


class LLMClient:
    """Unified interface for local LLMs."""

    def __init__(
        self,
        model: str = "llama3.2",
        provider: str = "ollama",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.3,
    ):
        self.model = model
        self.provider = provider.lower()
        self.temperature = temperature

        if self.provider == "ollama":
            self.base_url = base_url or "http://localhost:11434"
            self._client = None  # use ollama package
        else:
            # OpenAI-compatible (LM Studio default port 1234)
            self.base_url = (base_url or "http://localhost:1234/v1").rstrip("/")
            self.api_key = api_key or "lm-studio"
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=120.0,
            )

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
    ) -> Dict[str, Any]:
        """
        Returns a normalized response:
        {
          "content": str | None,
          "tool_calls": list[dict] | None,  # [{id, name, arguments}]
          "raw": original
        }
        """
        if self.provider == "ollama":
            return self._chat_ollama(messages, tools)
        return self._chat_openai_compat(messages, tools, tool_choice)

    def _chat_ollama(
        self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
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
            return {"content": f"[LLM error] {e}", "tool_calls": None, "raw": None}

        msg = resp.get("message", {})
        content = msg.get("content") or None
        tool_calls = None

        if msg.get("tool_calls"):
            tool_calls = []
            for tc in msg["tool_calls"]:
                fn = tc.get("function", {})
                args = fn.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {"raw": args}
                tool_calls.append(
                    {
                        "id": tc.get("id") or f"call_{len(tool_calls)}",
                        "name": fn.get("name", ""),
                        "arguments": args,
                    }
                )

        return {"content": content, "tool_calls": tool_calls, "raw": resp}

    def _chat_openai_compat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]],
        tool_choice: str,
    ) -> Dict[str, Any]:
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
        except Exception as e:
            return {"content": f"[LLM error] {e}", "tool_calls": None, "raw": None}

        choice = data["choices"][0]["message"]
        content = choice.get("content")
        tool_calls = None

        if choice.get("tool_calls"):
            tool_calls = []
            for tc in choice["tool_calls"]:
                fn = tc["function"]
                args = fn.get("arguments", "{}")
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {"raw": args}
                tool_calls.append(
                    {
                        "id": tc["id"],
                        "name": fn["name"],
                        "arguments": args,
                    }
                )

        return {"content": content, "tool_calls": tool_calls, "raw": data}

    def close(self) -> None:
        if self._client:
            self._client.close()
