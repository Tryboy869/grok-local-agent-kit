"""In-process TTL cache for tool results (v0.21)."""

from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


def cache_key(name: str, arguments: Dict[str, Any]) -> str:
    blob = json.dumps({"name": name, "args": arguments}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:24]


@dataclass
class CacheEntry:
    key: str
    name: str
    value: str
    created: float
    ttl: float
    hits: int = 0

    def expired(self, now: Optional[float] = None) -> bool:
        now = time.time() if now is None else now
        return now >= self.created + self.ttl


@dataclass
class ToolCache:
    ttl: float = 60.0
    max_entries: int = 256
    enabled: bool = True
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _store: Dict[str, CacheEntry] = field(default_factory=dict, repr=False)
    hits: int = 0
    misses: int = 0

    def get(self, name: str, arguments: Dict[str, Any]) -> Optional[str]:
        if not self.enabled:
            return None
        key = cache_key(name, arguments)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self.misses += 1
                return None
            if entry.expired():
                self._store.pop(key, None)
                self.misses += 1
                return None
            entry.hits += 1
            self.hits += 1
            return entry.value

    def put(self, name: str, arguments: Dict[str, Any], value: str, ttl: Optional[float] = None) -> str:
        if not self.enabled:
            return value
        key = cache_key(name, arguments)
        entry = CacheEntry(
            key=key,
            name=name,
            value=value,
            created=time.time(),
            ttl=self.ttl if ttl is None else ttl,
        )
        with self._lock:
            self._evict_unlocked()
            self._store[key] = entry
        return value

    def clear(self) -> int:
        with self._lock:
            n = len(self._store)
            self._store.clear()
            self.hits = 0
            self.misses = 0
            return n

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "enabled": self.enabled,
                "ttl": self.ttl,
                "size": len(self._store),
                "hits": self.hits,
                "misses": self.misses,
                "keys": [e.name for e in self._store.values()],
            }

    def _evict_unlocked(self) -> None:
        now = time.time()
        dead = [k for k, e in self._store.items() if e.expired(now)]
        for k in dead:
            self._store.pop(k, None)
        while len(self._store) >= self.max_entries:
            oldest = min(self._store.values(), key=lambda e: e.created)
            self._store.pop(oldest.key, None)


_CACHE = ToolCache()


def get_cache() -> ToolCache:
    return _CACHE


def reset_cache(ttl: float = 60.0, enabled: bool = True) -> ToolCache:
    global _CACHE
    _CACHE = ToolCache(ttl=ttl, enabled=enabled)
    return _CACHE


def cached_execute(
    name: str,
    arguments: Dict[str, Any],
    runner: Callable[[str, Dict[str, Any]], str],
    cache: Optional[ToolCache] = None,
) -> str:
    cache = cache or get_cache()
    hit = cache.get(name, arguments)
    if hit is not None:
        return hit
    value = runner(name, arguments)
    return cache.put(name, arguments, value)
