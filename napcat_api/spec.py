"""官方 API 规格（由 docs 同步生成）。"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).with_name("spec.json")


@lru_cache(maxsize=1)
def load_spec() -> dict:
    try:
        with SPEC_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {"version": "unknown", "actions": {}, "tags": []}


def spec_version() -> str:
    return str(load_spec().get("version") or "unknown")


def actions() -> dict:
    return load_spec().get("actions") or {}


def action_names() -> list[str]:
    return list(actions().keys())


def get_action(name: str) -> dict | None:
    return actions().get(name)


def tags() -> list[dict]:
    return load_spec().get("tags") or []


def search(keyword: str) -> list[dict]:
    keyword = (keyword or "").strip().lower()
    found = []
    for name, info in actions().items():
        haystack = " ".join(
            [name, info.get("summary") or "", info.get("description") or "", " ".join(info.get("tags") or [])]
        ).lower()
        if keyword in haystack:
            found.append({"action": name, **info})
    return found


def param_schema(name: str) -> dict:
    info = get_action(name) or {}
    schema = info.get("params")
    return schema if isinstance(schema, dict) else {}


def example(name: str):
    return (get_action(name) or {}).get("example")


def render_help(name: str) -> str:
    info = get_action(name)
    if not info:
        return f"未知 action：{name}"
    lines = [f"{name} — {info.get('summary') or ''}"]
    if info.get("description"):
        lines.append(info["description"])
    if info.get("tags"):
        lines.append("标签：" + "、".join(info["tags"]))
    props = (param_schema(name).get("properties") or {})
    required = set(param_schema(name).get("required") or [])
    if props:
        lines.append("参数：")
        for key, value in props.items():
            mark = "*" if key in required else " "
            typ = value.get("type") or ("ref" if "$ref" in value else "")
            desc = value.get("description") or ""
            lines.append(f"  {mark} {key}: {typ} {desc}".rstrip())
    ex = example(name)
    if ex is not None:
        lines.append("示例：" + json.dumps(ex, ensure_ascii=False))
    return "\n".join(lines)
