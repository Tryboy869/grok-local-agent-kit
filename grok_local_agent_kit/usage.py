"""Cheap token / call usage tracker for local runs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)


@dataclass
class UsageStats:
    llm_calls: int = 0
    tool_calls: int = 0
    prompt_chars: int = 0
    completion_chars: int = 0
    estimated_prompt_tokens: int = 0
    estimated_completion_tokens: int = 0

    def record_prompt(self, messages) -> None:
        blob = ""
        for m in messages or []:
            blob += str(m.get("content") or "")
        self.prompt_chars += len(blob)
        self.estimated_prompt_tokens += estimate_tokens(blob)
        self.llm_calls += 1

    def record_completion(self, text: str) -> None:
        text = text or ""
        self.completion_chars += len(text)
        self.estimated_completion_tokens += estimate_tokens(text)

    def record_tool(self) -> None:
        self.tool_calls += 1

    def as_dict(self) -> Dict[str, Any]:
        return {
            "llm_calls": self.llm_calls,
            "tool_calls": self.tool_calls,
            "prompt_chars": self.prompt_chars,
            "completion_chars": self.completion_chars,
            "estimated_prompt_tokens": self.estimated_prompt_tokens,
            "estimated_completion_tokens": self.estimated_completion_tokens,
        }

    def summary(self) -> str:
        d = self.as_dict()
        return (
            f"usage: llm={d['llm_calls']} tools={d['tool_calls']} "
            f"~prompt_tok={d['estimated_prompt_tokens']} "
            f"~completion_tok={d['estimated_completion_tokens']}"
        )
