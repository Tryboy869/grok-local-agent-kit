"""Opt-in live-model eval profile.

Default path is a deterministic stub so CI never talks to a model.
Set GROK_LIVE_EVAL=1 and pass live=True to hit Ollama / LM Studio.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

LIVE_ENV = "GROK_LIVE_EVAL"


@dataclass
class LiveCase:
    name: str
    prompt: str
    contains: Optional[str] = None
    json_key: Optional[str] = None
    max_chars: int = 4000


@dataclass
class LiveProfile:
    name: str
    cases: List[LiveCase] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "cases": [
                {
                    "name": c.name,
                    "prompt": c.prompt,
                    "contains": c.contains,
                    "json_key": c.json_key,
                    "max_chars": c.max_chars,
                }
                for c in self.cases
            ],
        }


@dataclass
class LiveResult:
    name: str
    passed: bool
    output: str
    error: str = ""
    backend: str = "stub"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "output": self.output[:500],
            "error": self.error,
            "backend": self.backend,
        }


DEFAULT_PROFILE = LiveProfile(
    name="smoke",
    cases=[
        LiveCase(
            name="echo-ok",
            prompt="Reply with the single word OK.",
            contains="OK",
        ),
        LiveCase(
            name="json-status",
            prompt='Reply with JSON only: {"status": "ready"}',
            json_key="status",
            contains="ready",
        ),
    ],
)


def live_enabled(flag: bool = False) -> bool:
    env = os.environ.get(LIVE_ENV, "").strip().lower() in {"1", "true", "yes", "on"}
    return bool(flag and env)


def stub_complete(prompt: str, case: Optional[LiveCase] = None) -> str:
    """Deterministic stand-in used when live models are disabled."""
    if case and case.json_key:
        value = case.contains or "ready"
        return json.dumps({case.json_key: value})
    if case and case.contains:
        return f"stub:{case.contains}"
    return f"stub:{prompt[:80]}"


def _score(case: LiveCase, text: str) -> tuple[bool, str]:
    clipped = text[: case.max_chars]
    if case.json_key:
        try:
            from .structured import extract_json_or_none

            parsed = extract_json_or_none(clipped)
        except Exception:
            parsed = None
            try:
                parsed = json.loads(clipped)
            except Exception:
                parsed = None
        if not isinstance(parsed, dict) or case.json_key not in parsed:
            return False, f"missing json key {case.json_key}"
        if case.contains and case.contains not in str(parsed[case.json_key]):
            return False, f"json key {case.json_key} missing {case.contains!r}"
        return True, ""
    if case.contains and case.contains not in clipped:
        return False, f"missing {case.contains!r}"
    return True, ""


def load_profile(path: Union[str, Path]) -> LiveProfile:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    cases = [
        LiveCase(
            name=item["name"],
            prompt=item["prompt"],
            contains=item.get("contains"),
            json_key=item.get("json_key"),
            max_chars=int(item.get("max_chars", 4000)),
        )
        for item in raw.get("cases", raw if isinstance(raw, list) else [])
    ]
    return LiveProfile(name=raw.get("name", Path(path).stem) if isinstance(raw, dict) else "file", cases=cases)


def run_profile(
    profile: Optional[LiveProfile] = None,
    *,
    live: bool = False,
    complete: Optional[Callable[[str], str]] = None,
) -> Dict[str, Any]:
    profile = profile or DEFAULT_PROFILE
    use_live = live_enabled(live)
    backend = "live" if use_live else "stub"
    results: List[LiveResult] = []

    def _call(case: LiveCase) -> str:
        if complete is not None:
            return complete(case.prompt)
        if use_live:
            from .llm import LLMClient

            client = LLMClient()
            return str(client.complete(case.prompt))
        return stub_complete(case.prompt, case)

    for case in profile.cases:
        try:
            output = _call(case)
            ok, err = _score(case, output)
            results.append(LiveResult(case.name, ok, output, err, backend))
        except Exception as exc:
            results.append(LiveResult(case.name, False, "", str(exc), backend))

    passed = sum(1 for r in results if r.passed)
    return {
        "profile": profile.name,
        "backend": backend,
        "live": use_live,
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "ok": passed == len(results) and len(results) > 0,
        "results": [r.as_dict() for r in results],
    }


def format_live_report(report: Dict[str, Any]) -> str:
    lines = [
        f"live-eval[{report.get('backend', '?')}] "
        f"{report['passed']}/{report['total']} passed "
        f"profile={report.get('profile', '')}"
    ]
    for item in report.get("results", []):
        mark = "PASS" if item["passed"] else "FAIL"
        extra = f" err={item['error']}" if item.get("error") else ""
        lines.append(f"  [{mark}] {item['name']}{extra}")
    return "\n".join(lines)


def demo_live_eval() -> str:
    return format_live_report(run_profile(DEFAULT_PROFILE, live=False))
