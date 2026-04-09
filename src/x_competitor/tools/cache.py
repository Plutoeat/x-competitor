"""搜索结果缓存 — 避免重复调用搜索 API"""

import hashlib
import json
import time
from pathlib import Path

from x_competitor.config import settings


def _cache_path(key: str) -> Path:
    h = hashlib.sha256(key.encode()).hexdigest()[:16]
    return settings.cache_dir / f"{h}.json"


def get(key: str) -> str | None:
    """读取缓存，过期则返回 None。"""
    path = _cache_path(key)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    age_hours = (time.time() - data["ts"]) / 3600
    if age_hours > settings.cache_ttl_hours:
        path.unlink()
        return None
    return data["result"]


def put(key: str, result: str) -> None:
    """写入缓存。"""
    settings.cache_dir.mkdir(parents=True, exist_ok=True)
    data = {"ts": time.time(), "result": result}
    _cache_path(key).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def purge_expired() -> int:
    """删除所有过期缓存文件，返回清理数量。"""
    if not settings.cache_dir.exists():
        return 0
    now = time.time()
    removed = 0
    for path in settings.cache_dir.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if (now - data["ts"]) / 3600 > settings.cache_ttl_hours:
                path.unlink()
                removed += 1
        except (json.JSONDecodeError, KeyError):
            path.unlink()
            removed += 1
    return removed