"""Extract JSON objects from LLM text — no extra deps."""

from __future__ import annotations

import json
import re
from typing import Any, Optional


_FENCE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)
_OBJECT = re.compile(r"\{[\s\S]*\}")
_ARRAY = re.compile(r"\[[\s\S]*\]")


def extract_json(text: str) -> Any:
    """Best-effort parse of the first JSON value in `text`.

    Tries fenced ```json blocks, then the first {...} or [...].
    Raises ValueError if nothing parses.
    """
    if not text or not str(text).strip():
        raise ValueError("empty text")
    raw = str(text).strip()
    candidates = []
    for m in _FENCE.finditer(raw):
        candidates.append(m.group(1).strip())
    candidates.append(raw)
    obj = _OBJECT.search(raw)
    if obj:
        candidates.append(obj.group(0))
    arr = _ARRAY.search(raw)
    if arr:
        candidates.append(arr.group(0))
    last_err: Optional[Exception] = None
    for c in candidates:
        try:
            return json.loads(c)
        except json.JSONDecodeError as exc:
            last_err = exc
            continue
    raise ValueError(f"no JSON found: {last_err}")


def extract_json_or_none(text: str) -> Optional[Any]:
    try:
        return extract_json(text)
    except ValueError:
        return None


def require_keys(payload: Any, keys: list[str]) -> dict:
    if not isinstance(payload, dict):
        raise ValueError(f"expected object, got {type(payload).__name__}")
    missing = [k for k in keys if k not in payload]
    if missing:
        raise ValueError(f"missing keys: {missing}")
    return payload
