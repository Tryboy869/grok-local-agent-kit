"""Web search with duckduckgo-search plus a no-dep HTML fallback."""

from __future__ import annotations

import re
from html import unescape
from typing import List, Tuple
from urllib.parse import quote_plus

import httpx

try:
    from duckduckgo_search import DDGS
except ImportError:  # pragma: no cover
    DDGS = None  # type: ignore

UA = "grok-local-agent-kit/0.27.0"


def _format(rows: List[Tuple[str, str, str]]) -> str:
    if not rows:
        return "No results found."
    lines = []
    for i, (title, href, body) in enumerate(rows, 1):
        lines.append(f"{i}. {title}\n   URL: {href}\n   {body}")
    return "\n\n".join(lines)


def _via_ddgs(query: str, max_results: int) -> List[Tuple[str, str, str]]:
    if DDGS is None:
        return []
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    out: List[Tuple[str, str, str]] = []
    for r in results:
        title = (r.get("title") or "No title").strip()
        href = (r.get("href") or "").strip()
        body = ((r.get("body") or "")[:250]).strip()
        if title or href:
            out.append((title, href, body))
    return out


_RESULT_RE = re.compile(
    r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
    re.I | re.S,
)
_SNIP_RE = re.compile(
    r'<a[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</a>',
    re.I | re.S,
)
_TAG_RE = re.compile(r"<[^>]+>")


def _strip(html: str) -> str:
    return unescape(_TAG_RE.sub("", html or "")).strip()


def _via_html(query: str, max_results: int) -> List[Tuple[str, str, str]]:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    with httpx.Client(timeout=12.0, follow_redirects=True) as client:
        r = client.get(url, headers={"User-Agent": UA})
        r.raise_for_status()
        html = r.text or ""
    titles = _RESULT_RE.findall(html)
    snips = [_strip(s) for s in _SNIP_RE.findall(html)]
    out: List[Tuple[str, str, str]] = []
    for i, (href, title_html) in enumerate(titles[:max_results]):
        body = snips[i][:250] if i < len(snips) else ""
        out.append((_strip(title_html) or "No title", href, body))
    return out


def search_web(query: str, max_results: int = 5) -> str:
    query = (query or "").strip()
    if not query:
        return "Error: query must be non-empty"
    max_results = max(1, min(int(max_results or 5), 10))
    last_err = ""
    try:
        rows = _via_ddgs(query, max_results)
        if rows:
            return _format(rows)
    except Exception as e:  # pragma: no cover
        last_err = str(e)
    try:
        rows = _via_html(query, max_results)
        if rows:
            return _format(rows)
    except Exception as e:
        last_err = last_err or str(e)
        return f"Search error: {e}"
    if last_err:
        return f"Search error: {last_err}"
    return "No results found."
