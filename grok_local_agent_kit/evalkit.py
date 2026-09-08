"""Offline eval harness: golden cases against tools / extractors, no LLM required."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from .structured import extract_json_or_none
from .tools import execute_tool


@dataclass
class EvalCase:
    name: str
    kind: str
    expect: Any
    tool: str = ""
    args: Dict[str, Any] = field(default_factory=dict)
    text: str = ""
    input: Any = None
    contains: Optional[str] = None


@dataclass
class EvalResult:
    name: str
    passed: bool
    actual: Any
    expect: Any
    error: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "actual": self.actual,
            "expect": self.expect,
            "error": self.error,
        }


def load_cases(path: Union[str, Path]) -> List[EvalCase]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "cases" in raw:
        raw = raw["cases"]
    cases: List[EvalCase] = []
    for item in raw:
        cases.append(
            EvalCase(
                name=item["name"],
                kind=item.get("kind", "tool"),
                expect=item.get("expect"),
                tool=item.get("tool", ""),
                args=item.get("args") or {},
                text=item.get("text", ""),
                input=item.get("input"),
                contains=item.get("contains"),
            )
        )
    return cases


def _match(actual: Any, case: EvalCase) -> bool:
    if case.contains is not None:
        return case.contains in str(actual)
    return actual == case.expect


def run_case(case: EvalCase) -> EvalResult:
    try:
        if case.kind == "tool":
            actual = execute_tool(case.tool, **case.args)
        elif case.kind == "json":
            actual = extract_json_or_none(case.text)
        elif case.kind == "equals":
            actual = case.input
        else:
            return EvalResult(case.name, False, None, case.expect, f"unknown kind {case.kind}")
        ok = _match(actual, case)
        return EvalResult(case.name, ok, actual, case.expect)
    except Exception as exc:
        return EvalResult(case.name, False, None, case.expect, str(exc))


def run_suite(cases: List[EvalCase], on_result: Optional[Callable[[EvalResult], None]] = None) -> Dict[str, Any]:
    results = []
    for case in cases:
        res = run_case(case)
        results.append(res)
        if on_result:
            on_result(res)
    passed = sum(1 for r in results if r.passed)
    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "ok": passed == len(results),
        "results": [r.as_dict() for r in results],
    }


def format_report(report: Dict[str, Any]) -> str:
    lines = [f"eval {report['passed']}/{report['total']} passed"]
    for item in report["results"]:
        mark = "PASS" if item["passed"] else "FAIL"
        extra = f" err={item['error']}" if item["error"] else ""
        lines.append(f"  [{mark}] {item['name']}{extra}")
    return "\n".join(lines)


DEFAULT_CASES: List[EvalCase] = [
    EvalCase(name="calc-21", kind="tool", tool="calculator", args={"expression": "3*7"}, expect="21"),
    EvalCase(
        name="json-fence",
        kind="json",
        text='noise\n```json\n{"ok": true}\n```\n',
        expect={"ok": True},
    ),
]
