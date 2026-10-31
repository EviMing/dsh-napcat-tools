"""NapCat 本地配置发现。

NapCat 的 OneBot11 HTTP 服务地址与 token 不在固定文件里，而是按 QQ 号分文件：
    <root>/napcat/config/onebot11_<qq>.json
本模块按优先级解析：

    1. 环境变量 NAPCAT_HTTP / NAPCAT_TOKEN / NAPCAT_QQ / NAPCAT_TIMEOUT
    2. NapCat 配置目录里已启用的 httpServers
    3. 默认 http://127.0.0.1:3000

版本号来源：
    - <root>/config.json 的 baseVersion / curVersion   -> QQ 本体版本
    - napcat_api/version.json                              -> 上次探测到的 NapCat 版本
    - 在线 get_version_info                                -> 最准，cli version 会刷新缓存
"""

from __future__ import annotations

import glob
import json
import os
from datetime import datetime
from pathlib import Path

DEFAULT_ROOT = Path(os.environ.get("NAPCAT_ROOT") or r"D:\NapCat")
DEFAULT_TIMEOUT = float(os.environ.get("NAPCAT_TIMEOUT") or 30)
VERSION_CACHE = Path(__file__).with_name("version.json")

_CANDIDATE_ROOTS = [
    DEFAULT_ROOT,
    Path(r"D:\NapCat"),
    Path(r"C:\NapCat"),
    Path(os.path.expanduser(r"~\NapCat")),
]


def find_root() -> Path | None:
    """返回第一个存在的 NapCat 安装目录。"""
    for root in _CANDIDATE_ROOTS:
        if (root / "napcat" / "config").is_dir():
            return root
    return None


def _read_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8-sig") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def qq_version(root: Path | None = None) -> dict:
    """读取 D:\\NapCat\\config.json 里记录的 QQ 版本（NapCat 启动器写入）。"""
    root = root or find_root()
    if not root:
        return {}
    data = _read_json(root / "config.json")
    return {
        "base_version": data.get("baseVersion"),
        "cur_version": data.get("curVersion"),
        "build_id": data.get("buildId"),
    }


def _onebot11_files(root: Path) -> list[Path]:
    cfg = root / "napcat" / "config"
    return sorted(Path(p) for p in glob.glob(str(cfg / "onebot11_*.json")))


def http_candidates(root: Path | None = None) -> list[dict]:
    """列出本机所有启用中的 OneBot11 HTTP 服务端。"""
    root = root or find_root()
    if not root:
        return []
    out: list[dict] = []
    for path in _onebot11_files(root):
        data = _read_json(path)
        network = data.get("network") or {}
        qq = path.stem.replace("onebot11_", "")
        for server in network.get("httpServers") or []:
            if not server.get("enable", True):
                continue
            host = server.get("host") or "127.0.0.1"
            if host in ("0.0.0.0", "::"):
                host = "127.0.0.1"
            port = int(server.get("port") or 3000)
            out.append(
                {
                    "qq": qq,
                    "name": server.get("name") or "",
                    "host": host,
                    "port": port,
                    "token": server.get("token") or "",
                    "base_url": f"http://{host}:{port}",
                    "file": str(path),
                }
            )
    return out


def resolve() -> dict:
    """解析出当前要用的 OneBot HTTP 地址、token、账号与版本信息。"""
    root = find_root()
    candidates = http_candidates(root)
    env_qq = os.environ.get("NAPCAT_QQ")
    chosen = None
    if env_qq:
        chosen = next((c for c in candidates if c["qq"] == env_qq), None)
    if chosen is None:
        chosen = candidates[0] if candidates else None

    base_url = os.environ.get("NAPCAT_HTTP") or (chosen or {}).get("base_url") or "http://127.0.0.1:3000"
    token = os.environ.get("NAPCAT_TOKEN")
    if token is None:
        token = (chosen or {}).get("token") or ""
    try:
        timeout = float(os.environ.get("NAPCAT_TIMEOUT") or DEFAULT_TIMEOUT)
    except ValueError:
        timeout = DEFAULT_TIMEOUT

    cache = _read_json(VERSION_CACHE)
    return {
        "root": str(root) if root else None,
        "base_url": base_url.rstrip("/"),
        "token": token,
        "timeout": timeout,
        "qq": (chosen or {}).get("qq") or env_qq,
        "server_name": (chosen or {}).get("name"),
        "config_file": (chosen or {}).get("file"),
        "qq_version": qq_version(root),
        "napcat_version": os.environ.get("NAPCAT_VERSION") or cache.get("napcat_version"),
        "candidates": candidates,
    }


def save_napcat_version(version: str, source: str = "get_version_info") -> None:
    """把探测到的 NapCat 版本写入本地缓存文件。"""
    if not version:
        return
    data = _read_json(VERSION_CACHE)
    data.update(
        {
            "napcat_version": version,
            "qq_version": qq_version().get("cur_version") or data.get("qq_version"),
            "source": source,
            "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        }
    )
    try:
        VERSION_CACHE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass
