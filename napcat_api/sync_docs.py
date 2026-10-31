"""按本地 NapCat 版本同步官方 OpenAPI 文档。

官方文档站 https://napneko.github.io/api/<版本> 是 VitePress 页面，真正的 OpenAPI
JSON 被切成了 /assets/chunks/openapi.<hash>.js。本模块按同样路径把它取回来，
转成 napcat_api/spec.json，并记录版本号到 version.json。

用法：
    python -m napcat_api sync-docs            # 用本地/在线版本同步
    python -m napcat_api sync-docs 4.18.42    # 指定版本
    python -m napcat_api sync-docs --check    # 只检查版本是否一致
"""

from __future__ import annotations

import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from . import config, spec

SITE = "https://napneko.github.io"
SPEC_FILE = Path(__file__).with_name("spec.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) napcat-api-sync/1.0"


class SyncError(RuntimeError):
    pass


def _fetch(url: str, timeout: float = 60) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return resp.read().decode("utf-8", "replace")
    except ssl.SSLError:
        # 本机可能有 TLS 中间层（例如 Steam++ / 抓包代理），退回不校验证书。
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(request, timeout=timeout, context=ctx) as resp:
            return resp.read().decode("utf-8", "replace")


def latest_version() -> str:
    html = _fetch(f"{SITE}/api/")
    found = re.findall(r"/api/(\d+\.\d+\.\d+)", html)
    if not found:
        raise SyncError("官方文档首页没有解析到任何版本号")
    return found[0]


def _entry_js(version: str) -> str:
    html = _fetch(f"{SITE}/api/{version}")
    match = re.search(r"assets/(api_" + re.escape(version) + r"\.md\.[A-Za-z0-9_-]+\.lean\.js)", html)
    if not match:
        raise SyncError(f"页面里找不到 {version} 的入口脚本（文档结构可能变了）")
    return match.group(1)


def _spec_chunk(entry: str, version: str) -> str:
    js = _fetch(f"{SITE}/assets/{entry}")
    patterns = [
        r'"\./' + re.escape(version) + r'/openapi\.json":\(\)=>[^(]*\(\(\)=>import\("([^"]+)"\)',
        r'"\./' + re.escape(version) + r'/openapi\.json":\(\)=>import\("([^"]+)"\)',
    ]
    for pattern in patterns:
        match = re.search(pattern, js)
        if match:
            return match.group(1).removeprefix("./")
    raise SyncError(f"入口脚本里找不到 {version} 的 openapi 分块")


def _node_available(node: str) -> bool:
    return shutil.which(node) is not None


def _chunk_to_json(chunk_js: str, node: str) -> dict:
    """用 node 动态 import 官方分块，拿到真正的 OpenAPI 对象。

    注意：这里不用 subprocess 的管道（capture_output）。Windows 沙箱会拒绝
    CreatePipe（WinError 5），所以把 node 的 stdout/stderr 重定向到文件再读。
    """
    # 不写系统临时目录：Windows 沙箱/杀毒可能拒绝在该目录新建或删除文件，
    # 写到包目录旁边最稳，退出时尽力清理。
    base_dir = Path(__file__).parent
    fd, raw_path = tempfile.mkstemp(prefix=".spec_", suffix=".mjs", dir=str(base_dir))
    path = Path(raw_path)
    out_path: Path | None = None
    err_path: Path | None = None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(chunk_js)
        uri = path.resolve().as_uri()
        code = (
            f"import spec from {json.dumps(uri)};"
            "process.stdout.write(JSON.stringify(spec));"
        )
        out_fd, out_raw = tempfile.mkstemp(prefix=".spec_out_", suffix=".json", dir=str(base_dir))
        err_fd, err_raw = tempfile.mkstemp(prefix=".spec_err_", suffix=".txt", dir=str(base_dir))
        out_path, err_path = Path(out_raw), Path(err_raw)
        with os.fdopen(out_fd, "wb") as out_fh, os.fdopen(err_fd, "wb") as err_fh:
            proc = subprocess.run(
                [node, "--input-type=module", "-e", code],
                stdout=out_fh,
                stderr=err_fh,
                timeout=120,
            )
        if proc.returncode != 0:
            detail = err_path.read_text(encoding="utf-8", errors="replace")[:500]
            raise SyncError(f"node 解析官方分块失败：{detail}")
        try:
            return json.loads(out_path.read_text(encoding="utf-8", errors="replace"))
        except ValueError as exc:
            raise SyncError(f"node 输出不是 JSON：{exc}") from exc
    finally:
        for candidate in (path, out_path, err_path):
            if candidate is None:
                continue
            try:
                candidate.unlink(missing_ok=True)
            except OSError:
                pass


def _trim(raw: dict) -> dict:
    actions = {}
    for path, item in (raw.get("paths") or {}).items():
        post = item.get("post") or item.get("get")
        if not post:
            continue
        body = ((post.get("requestBody") or {}).get("content") or {}).get("application/json") or {}
        actions[path.lstrip("/")] = {
            "summary": post.get("summary") or "",
            "description": post.get("description") or "",
            "deprecated": bool(post.get("deprecated")),
            "tags": post.get("tags") or [],
            "params": body.get("schema"),
            "example": ((body.get("examples") or {}).get("Default") or {}).get("value"),
        }
    info = raw.get("info") or {}
    return {
        "title": info.get("title"),
        "version": info.get("version"),
        "description": info.get("description"),
        "openapi": raw.get("openapi"),
        "source": f"{SITE}/api/{info.get('version')}",
        "tags": raw.get("tags") or [],
        "actions": actions,
    }


def resolve_target_version(version: str | None, node: str) -> str:
    if version:
        return version
    cfg = config.resolve()
    if cfg.get("napcat_version"):
        return str(cfg["napcat_version"])
    # 没缓存就用在线探测；NapCat 不在线则退回文档最新版。
    try:
        from .client import NapCatClient

        data = NapCatClient().call("get_version_info") or {}
        if data.get("app_version"):
            return str(data["app_version"])
    except Exception:
        pass
    return latest_version()


def run(version: str | None = None, check: bool = False, node: str = "node", as_json: bool = False) -> int:
    try:
        target = resolve_target_version(version, node)
        local = spec.spec_version()
        if check:
            same = target == local
            payload = {"target": target, "local": local, "match": same}
            print(json.dumps(payload, ensure_ascii=False, indent=2) if as_json else
                  (f"一致：{local}" if same else f"不一致：文档 {target} / 本地缓存 {local}"))
            return 0 if same else 1
        if target == local and SPEC_FILE.exists():
            print(f"已是最新：{local}，无需同步")
            return 0
        print(f"同步 NapCat {target} 官方 API 文档…")
        entry = _entry_js(target)
        chunk = _spec_chunk(entry, target)
        raw = _chunk_to_json(_fetch(f"{SITE}/assets/{chunk}"), node)
        trimmed = _trim(raw)
        if trimmed["version"] != target:
            trimmed["version"] = target
        SPEC_FILE.write_text(json.dumps(trimmed, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        config.save_napcat_version(target, "docs")
        n = len(trimmed["actions"])
        payload = {"version": trimmed["version"], "actions": n, "file": str(SPEC_FILE)}
        if as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"完成：{trimmed['version']}，{n} 个 action -> {SPEC_FILE}")
        return 0
    except (SyncError, OSError, subprocess.SubprocessError) as exc:
        if as_json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        print(f"[同步失败] {exc}", file=sys.stderr)
        return 1
