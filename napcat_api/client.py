"""NapCat OneBot 11 HTTP 客户端。"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Any

from . import config
from .spec import get_action


class NapCatError(RuntimeError):
    """调用 NapCat / OneBot 失败。"""

    def __init__(
        self,
        action: str,
        message: str,
        *,
        retcode: int | None = None,
        status: str | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(f"[{action}] {message}")
        self.action = action
        self.retcode = retcode
        self.status = status
        self.payload = payload


class NapCatClient:
    """一个账号的 OneBot 11 客户端。

    所有官方 action 都可以直接当方法用：

        client.send_group_msg(group_id=123, message="hi")
        client.get_group_list()
        client.call("send_private_msg", {"user_id": 1, "message": "hi"})
    """

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
        timeout: float | None = None,
    ) -> None:
        resolved = config.resolve()
        self.base_url = (base_url or resolved["base_url"]).rstrip("/")
        self.token = resolved["token"] if token is None else token
        self.timeout = timeout or resolved["timeout"]
        self.qq = resolved.get("qq")

    # ------------------------------------------------------------------ 核心
    def raw_call(self, action: str, params: dict | None = None, timeout: float | None = None) -> dict:
        """POST 一个 action，返回 NapCat 的完整响应（不抛 retcode 业务错误）。"""
        body = json.dumps(params or {}, ensure_ascii=False).encode("utf-8")
        url = f"{self.base_url}/{action}"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "User-Agent": "napcat-api-python/1.0",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                text = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            try:
                payload = json.loads(detail)
                message = payload.get("message") or payload.get("wording") or detail
            except ValueError:
                payload, message = None, detail or str(exc)
            raise NapCatError(action, f"HTTP {exc.code}: {message}", status=str(exc.code), payload=payload) from exc
        except urllib.error.URLError as exc:
            raise NapCatError(
                action,
                f"连不上 NapCat（{self.base_url}）：{exc.reason}；请确认 NapCat 已启动、端口和 token 正确",
            ) from exc
        except TimeoutError as exc:
            raise NapCatError(action, f"请求超时（{timeout or self.timeout}s）：{self.base_url}") from exc
        try:
            return json.loads(text)
        except ValueError as exc:
            raise NapCatError(action, f"响应不是 JSON：{text[:300]}") from exc

    def call(self, action: str, params: dict | None = None, timeout: float | None = None) -> Any:
        """调用一个 action，成功返回 data，失败抛 NapCatError。"""
        info = get_action(action)
        if info is None:
            hint = _closest_action(action)
            raise NapCatError(action, f"官方 API 里没有这个 action{'；你是不是想要 ' + hint if hint else ''}")
        payload = self.raw_call(action, params, timeout)
        status = payload.get("status")
        retcode = payload.get("retcode")
        if status not in (None, "ok") or retcode not in (None, 0):
            message = payload.get("message") or payload.get("wording") or f"retcode={retcode}"
            raise NapCatError(action, str(message), retcode=retcode, status=status, payload=payload)
        return payload.get("data")

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        if get_action(name) is None:
            raise AttributeError(f"NapCat 没有 action：{name}")

        def _call(**kwargs: Any) -> Any:
            return self.call(name, kwargs)

        _call.__name__ = name
        _call.__doc__ = (get_action(name) or {}).get("description") or ""
        return _call

    # ------------------------------------------------------------- 便捷封装
    def send_private(self, user_id: int, message: Any, **kwargs: Any) -> Any:
        return self.call("send_private_msg", {"user_id": int(user_id), "message": message, **kwargs})

    def send_group(self, group_id: int, message: Any, **kwargs: Any) -> Any:
        return self.call("send_group_msg", {"group_id": int(group_id), "message": message, **kwargs})

    def send_to(self, target: str, message: Any, **kwargs: Any) -> Any:
        """target 形如 group:123 / private:123 / u123 / g123。"""
        kind, ident = parse_target(target)
        if kind == "group":
            return self.send_group(ident, message, **kwargs)
        return self.send_private(ident, message, **kwargs)


def parse_target(target: str) -> tuple[str, int]:
    text = str(target).strip()
    match = re.fullmatch(r"(?i)(group|private|user|g|u|p)\s*[:/]?\s*(\d+)", text)
    if match:
        kind = "group" if match.group(1).lower().startswith("g") else "private"
        return kind, int(match.group(2))
    if text.isdigit():
        raise ValueError("纯数字目标有歧义，请写成 group:123 或 user:123")
    raise ValueError(f"无法解析目标：{target}")


def _closest_action(name: str) -> str | None:
    from difflib import get_close_matches

    from .spec import action_names

    matches = get_close_matches(name, action_names(), n=1, cutoff=0.6)
    return matches[0] if matches else None


def call(action: str, params: dict | None = None, **kwargs: Any) -> Any:
    """模块级快捷调用：call('get_group_list')。"""
    if kwargs:
        params = {**(params or {}), **kwargs}
    return NapCatClient().call(action, params)
