"""OneBot 11 消息段构造器。

官方消息段文档：https://napneko.github.io/onebot/segment
所有函数返回 {"type": ..., "data": {...}}，可以直接组成 message 数组。
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Any, Iterable


def seg(type_: str, **data: Any) -> dict:
    return {"type": type_, "data": {k: v for k, v in data.items() if v is not None}}


def text(content: Any) -> dict:
    return seg("text", text=str(content))


def at(qq: int | str, name: str | None = None) -> dict:
    return seg("at", qq=str(qq), name=name)


def at_all() -> dict:
    return at("all")


def reply(message_id: int | str) -> dict:
    return seg("reply", id=str(message_id))


def face(face_id: int | str) -> dict:
    return seg("face", id=str(face_id))


def _media(source: str | os.PathLike, *, allow_base64: bool = True) -> str:
    raw = str(source)
    if raw.startswith(("http://", "https://", "base64://", "file://", "data:")):
        return raw
    path = Path(raw).expanduser()
    if path.is_file():
        if not allow_base64:
            return str(path.resolve())
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        payload = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"base64://{payload}"
    raise FileNotFoundError(f"媒体文件不存在：{raw}")


def image(source: str | os.PathLike) -> dict:
    return seg("image", file=_media(source))


def record(source: str | os.PathLike) -> dict:
    return seg("record", file=_media(source))


def video(source: str | os.PathLike) -> dict:
    return seg("video", file=_media(source))


def file(source: str | os.PathLike, name: str | None = None) -> dict:
    raw = str(source)
    if raw.startswith(("http://", "https://", "base64://", "file://")):
        value = raw
    else:
        path = Path(raw).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"文件不存在：{raw}")
        value = str(path.resolve())
    return seg("file", file=value, name=name or Path(raw).name)


def json_card(data: Any) -> dict:
    if not isinstance(data, str):
        data = json.dumps(data, ensure_ascii=False)
    return seg("json", data=data)


def markdown(content: str) -> dict:
    return seg("markdown", content=content)


def forward_id(forward_id_value: str) -> dict:
    return seg("forward", id=str(forward_id_value))


def node(user_id: int | str, nickname: str, content: Any) -> dict:
    message = content if isinstance(content, list) else [text(content)]
    return seg("node", user_id=str(user_id), nickname=nickname, content=message)


def forward_nodes(nodes: Iterable[dict]) -> dict:
    return seg("forward", messages=list(nodes))


def normalize(message: Any) -> Any:
    """把字符串/单个段/段数组统一成 NapCat 接受的形式。"""
    if isinstance(message, str):
        return [text(message)]
    if isinstance(message, dict):
        return [message]
    if isinstance(message, list):
        return message
    raise TypeError(f"无法识别的 message：{type(message).__name__}")


def preview(message: Any, limit: int = 120) -> str:
    """给 CLI 打印用的简短消息预览。"""
    parts = []
    for item in normalize(message) if message is not None else []:
        if not isinstance(item, dict):
            parts.append(str(item))
            continue
        data = item.get("data") or {}
        t = item.get("type")
        if t == "text":
            parts.append(str(data.get("text", "")))
        elif t == "at":
            parts.append(f"@{data.get('name') or data.get('qq')}")
        elif t == "reply":
            parts.append(f"[回复 {data.get('id')}]")
        elif t in ("image", "record", "video", "file"):
            parts.append(f"[{t}]")
        else:
            parts.append(f"[{t}]")
    out = "".join(parts)
    return out if len(out) <= limit else out[: limit - 1] + "…"
