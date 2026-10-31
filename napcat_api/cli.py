"""命令行入口：python -m napcat_api <命令>。

设计目标：官方文档里的每一个 action 都能通过 `call` 直接调用；高频操作再给一层
更好用的快捷命令（send / groups / history …）。所有命令都支持 `--json` 输出，
方便 DeepSeek Harness 直接解析。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from typing import Any

from . import config, segments, spec
from .client import NapCatClient, NapCatError

EXIT_OK = 0
EXIT_ERROR = 2


# --------------------------------------------------------------------- 输出
def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str))


def emit(value: Any, as_json: bool, human: str | None = None) -> None:
    if as_json:
        _print_json(value)
    elif human is not None:
        print(human)
    else:
        _print_json(value)


def _fmt_time(ts: Any) -> str:
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError, OSError):
        return str(ts or "")


def _message_text(message: Any) -> str:
    if isinstance(message, str):
        return message
    if isinstance(message, list):
        return segments.preview(message, limit=200)
    return str(message)


def format_message(msg: dict) -> str:
    sender = msg.get("sender") or {}
    who = sender.get("card") or sender.get("nickname") or sender.get("user_id") or "?"
    uid = sender.get("user_id") or msg.get("user_id") or ""
    body = _message_text(msg.get("message") if "message" in msg else msg.get("raw_message"))
    return f"[{msg.get('message_id', '?')}] {_fmt_time(msg.get('time'))} {who}({uid}): {body}"


def format_messages(data: Any) -> str:
    if isinstance(data, dict):
        data = data.get("messages") or data.get("message") or []
    if not isinstance(data, list):
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)
    return "\n".join(format_message(m) for m in data if isinstance(m, dict))


# --------------------------------------------------------------------- 参数
def coerce(text: str) -> Any:
    stripped = text.strip()
    low = stripped.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "none"):
        return None
    if stripped.startswith(("[", "{")):
        try:
            return json.loads(stripped)
        except ValueError:
            return text
    try:
        return int(stripped)
    except ValueError:
        pass
    try:
        return float(stripped)
    except ValueError:
        return text


def extract_global(argv: list[str]) -> tuple[list[str], dict]:
    """把 --base/--token/--timeout/--json 从任意位置摘出来，其余交给 argparse。"""
    opts = {"base": None, "token": None, "timeout": None, "as_json": False}
    rest: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--json":
            opts["as_json"] = True
        elif arg.startswith("--base="):
            opts["base"] = arg.split("=", 1)[1]
        elif arg == "--base" and i + 1 < len(argv):
            i += 1
            opts["base"] = argv[i]
        elif arg.startswith("--token="):
            opts["token"] = arg.split("=", 1)[1]
        elif arg == "--token" and i + 1 < len(argv):
            i += 1
            opts["token"] = argv[i]
        elif arg.startswith("--timeout="):
            opts["timeout"] = float(arg.split("=", 1)[1])
        elif arg == "--timeout" and i + 1 < len(argv):
            i += 1
            opts["timeout"] = float(argv[i])
        else:
            rest.append(arg)
        i += 1
    return rest, opts


# --------------------------------------------------------------------- parser
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m napcat_api",
        description="NapCat OneBot 11 命令行封装（官方 API 4.x 全量 action）",
        epilog='示例：python -m napcat_api send -g 123456 -t "你好"；python -m napcat_api call get_group_list',
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("version", help="本地配置 + NapCat/QQ 版本")
    p.add_argument("--check", action="store_true", help="在线调用 get_version_info 刷新并写回 version.json")

    sub.add_parser("whoami", help="当前登录账号")
    sub.add_parser("status", help="NapCat 运行状态")

    p = sub.add_parser("groups", help="群列表")
    p.add_argument("--no-cache", action="store_true")

    sub.add_parser("friends", help="好友列表")

    p = sub.add_parser("members", help="群成员列表")
    p.add_argument("group_id", type=int)

    p = sub.add_parser("group-info", help="群信息")
    p.add_argument("group_id", type=int)

    p = sub.add_parser("history", help="聊天记录")
    p.add_argument("--group", "-g", type=int)
    p.add_argument("--user", "-u", type=int)
    p.add_argument("--count", "-n", type=int, default=20)
    p.add_argument("--message-seq", type=int, default=None)

    p = sub.add_parser("send", help="发消息（文本/图片/语音/视频/文件/@/回复）")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--group", "-g", type=int, help="群号")
    target.add_argument("--user", "-u", type=int, help="QQ 号")
    p.add_argument("--text", "-t", action="append", default=[], help="文本，可重复")
    p.add_argument("--image", action="append", default=[], help="图片：本地路径/URL/base64://，可重复")
    p.add_argument("--record", action="append", default=[], help="语音，可重复")
    p.add_argument("--video", action="append", default=[], help="视频，可重复")
    p.add_argument("--file", action="append", default=[], help="文件，可重复")
    p.add_argument("--at", action="append", default=[], help="要 @ 的 QQ，可重复")
    p.add_argument("--reply", type=int, default=None, help="引用回复的消息 id")
    p.add_argument("--face", action="append", default=[], help="表情 id，可重复")
    p.add_argument("--json-card", default=None, help="JSON 卡片内容（字符串或 JSON）")
    p.add_argument("--markdown", default=None, help="markdown 内容")
    p.add_argument("--dry-run", action="store_true", help="只打印构造出的请求，不发送")

    p = sub.add_parser("call", help="直接调用官方 action（任意参数）")
    p.add_argument("action")
    p.add_argument("--params", "-p", default=None, help="JSON 对象，例如 '{\"group_id\":123}'")
    p.add_argument("--params-file", default=None, help="从文件读取 JSON 参数")
    p.add_argument("--param", "-P", action="append", default=[], metavar="K=V", help="单个参数，可重复")
    p.add_argument("--force", action="store_true", help="不校验参数名是否在文档里")

    p = sub.add_parser("actions", help="列出全部 action")
    p.add_argument("--tag", default=None, help="按分类过滤")
    p.add_argument("--search", default=None, help="按关键词过滤")

    p = sub.add_parser("doc", help="查看某个 action 的参数")
    p.add_argument("action")

    p = sub.add_parser("sync-docs", help="按本地 NapCat 版本同步官方 OpenAPI 文档")
    p.add_argument("version", nargs="?", default=None)
    p.add_argument("--check", action="store_true")
    p.add_argument("--node", default="node")

    return parser


# --------------------------------------------------------------------- 命令
def cmd_version(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    live: dict = {}
    if args.check:
        try:
            live = client.call("get_version_info") or {}
            config.save_napcat_version(str(live.get("app_version") or ""), "get_version_info")
        except NapCatError as exc:
            live = {"error": str(exc)}
    out = {
        "root": cfg.get("root"),
        "base_url": cfg.get("base_url"),
        "qq": cfg.get("qq"),
        "token_set": bool(cfg.get("token")),
        "qq_version": cfg.get("qq_version"),
        "napcat_version": cfg.get("napcat_version"),
        "docs_version": spec.spec_version(),
        "action_count": len(spec.action_names()),
        "live": live,
    }
    human = (
        f"NapCat 根目录 : {cfg.get('root')}\n"
        f"OneBot HTTP  : {cfg.get('base_url')}（token {'已配置' if cfg.get('token') else '未配置'}）\n"
        f"账号         : {cfg.get('qq') or '-'}\n"
        f"QQ 版本      : {(cfg.get('qq_version') or {}).get('cur_version') or '-'}\n"
        f"NapCat 版本  : {cfg.get('napcat_version') or (live.get('app_version') if isinstance(live, dict) else None) or '-'}\n"
        f"文档版本     : {spec.spec_version()}（{len(spec.action_names())} 个 action）"
    )
    if isinstance(live, dict) and live.get("app_version"):
        human += f"\n在线探测     : {live['app_version']} / {live.get('protocol_version')}"
        if live["app_version"] != spec.spec_version():
            human += f"\n提示         : 官方文档版本与本地不一致，建议 python -m napcat_api sync-docs"
    emit(out, as_json, human)
    return EXIT_OK


def cmd_whoami(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    data = client.call("get_login_info") or {}
    emit(data, as_json, f"{data.get('nickname', '')}({data.get('user_id', '')})")
    return EXIT_OK


def cmd_status(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    data = client.call("get_status") or {}
    emit(data, as_json)
    return EXIT_OK


def cmd_groups(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    params = {"no_cache": True} if args.no_cache else {}
    data = client.call("get_group_list", params) or []
    human = "\n".join(
        f"{g.get('group_id')} {g.get('group_name')} ({g.get('member_count', '?')}人)" for g in data
    )
    emit(data, as_json, human)
    return EXIT_OK


def cmd_friends(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    data = client.call("get_friend_list") or []
    human = "\n".join(f"{f.get('user_id')} {f.get('nickname', '')} {f.get('remark', '')}".rstrip() for f in data)
    emit(data, as_json, human)
    return EXIT_OK


def cmd_members(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    data = client.call("get_group_member_list", {"group_id": args.group_id}) or []
    human = "\n".join(
        f"{m.get('user_id')} {m.get('card') or m.get('nickname') or ''} ({m.get('role', '')})" for m in data
    )
    emit(data, as_json, human)
    return EXIT_OK


def cmd_group_info(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    data = client.call("get_group_info", {"group_id": args.group_id}) or {}
    human = f"{data.get('group_id')} {data.get('group_name')} ({data.get('member_count', '?')}人)"
    emit(data, as_json, human)
    return EXIT_OK


def cmd_history(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    if args.group is None and args.user is None:
        raise SystemExit("history 需要 --group 或 --user")
    if args.group is not None:
        data = client.call(
            "get_group_msg_history",
            {"group_id": args.group, "count": args.count, **({"message_seq": args.message_seq} if args.message_seq else {})},
        )
    else:
        data = client.call(
            "get_friend_msg_history",
            {"user_id": args.user, "count": args.count, **({"message_seq": args.message_seq} if args.message_seq else {})},
        )
    emit(data, as_json, format_messages(data))
    return EXIT_OK


def mask_payload(value: Any) -> Any:
    """把超长的 base64 媒体换成占位符，避免 dry-run 刷屏。"""
    if isinstance(value, dict):
        return {k: mask_payload(v) for k, v in value.items()}
    if isinstance(value, list):
        return [mask_payload(v) for v in value]
    if isinstance(value, str) and len(value) > 300:
        return f"<{len(value)} chars>"
    return value


def cmd_send(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    message: list[dict] = []
    if args.reply is not None:
        message.append(segments.reply(args.reply))
    for qq in args.at:
        message.append(segments.at(qq))
    for value in args.text:
        message.append(segments.text(value))
    for value in args.face:
        message.append(segments.face(value))
    for value in args.image:
        message.append(segments.image(value))
    for value in args.record:
        message.append(segments.record(value))
    for value in args.video:
        message.append(segments.video(value))
    for value in args.file:
        message.append(segments.file(value))
    if args.json_card:
        raw = args.json_card
        try:
            raw = json.loads(raw)
        except ValueError:
            pass
        message.append(segments.json_card(raw))
    if args.markdown:
        message.append(segments.markdown(args.markdown))
    if not message:
        raise SystemExit("至少要给出 --text/--image/--record/--video/--file/--at/--json-card 之一")

    action = "send_group_msg" if args.group is not None else "send_private_msg"
    params = {
        "group_id": args.group,
        "user_id": args.user,
        "message": message,
    }
    params = {k: v for k, v in params.items() if v is not None}
    if args.dry_run:
        safe = mask_payload(params)
        preview = json.dumps(safe, ensure_ascii=False)
        target = f"group:{args.group}" if args.group is not None else f"user:{args.user}"
        emit(safe, as_json, f"[dry-run] {action} -> {target}\n{preview}")
        return EXIT_OK
    data = client.call(action, params) or {}
    human = f"已发送 message_id={data.get('message_id')} -> {args.group if args.group is not None else args.user}: {segments.preview(message)}"
    emit(data, as_json, human)
    return EXIT_OK


def cmd_call(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    params: dict = {}
    if args.params_file:
        try:
            with open(args.params_file, "r", encoding="utf-8-sig") as fh:
                loaded = json.load(fh)
        except (OSError, ValueError) as exc:
            raise SystemExit(f"读取 --params-file 失败：{exc}")
        if not isinstance(loaded, dict):
            raise SystemExit("--params-file 必须是 JSON 对象")
        params.update(loaded)
    if args.params:
        try:
            loaded = json.loads(args.params)
        except ValueError as exc:
            raise SystemExit(f"--params 不是合法 JSON：{exc}")
        if not isinstance(loaded, dict):
            raise SystemExit("--params 必须是 JSON 对象")
        params.update(loaded)
    for pair in args.param:
        if "=" not in pair:
            raise SystemExit(f"--param 需要 K=V：{pair}")
        key, value = pair.split("=", 1)
        params[key.strip()] = coerce(value)

    schema = spec.param_schema(args.action)
    known = (schema.get("properties") or {})
    if known and not args.force:
        unknown = [k for k in params if k not in known]
        if unknown:
            raise SystemExit(f"参数不在官方文档里：{', '.join(unknown)}（确认要传就加 --force）")

    data = client.call(args.action, params)
    if not as_json and spec.get_action(args.action) is None:
        _print_json(data)
    else:
        emit(data, as_json)
    return EXIT_OK


def cmd_actions(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    items = spec.search(args.search) if args.search else [{"action": n, **spec.get_action(n)} for n in spec.action_names()]
    if args.tag:
        items = [i for i in items if args.tag in (i.get("tags") or [])]
    if as_json:
        _print_json([{"action": i["action"], "summary": i.get("summary"), "tags": i.get("tags")} for i in items])
        return EXIT_OK
    by_tag: dict[str, list[dict]] = {}
    for item in items:
        for tag in item.get("tags") or ["未分类"]:
            by_tag.setdefault(tag, []).append(item)
    lines = [f"共 {len(items)} 个 action（文档版本 {spec.spec_version()}）"]
    for tag, group in by_tag.items():
        lines.append(f"\n## {tag}（{len(group)}）")
        for item in group:
            lines.append(f"  {item['action']:<32} {item.get('summary') or ''}")
    print("\n".join(lines))
    return EXIT_OK


def cmd_doc(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    info = spec.get_action(args.action)
    if info is None:
        raise SystemExit(f"未知 action：{args.action}")
    if as_json:
        _print_json({"action": args.action, **info})
    else:
        print(spec.render_help(args.action))
    return EXIT_OK


def cmd_sync_docs(client: NapCatClient, args, cfg: dict, as_json: bool) -> int:
    from . import sync_docs

    return sync_docs.run(version=args.version, check=args.check, node=args.node, as_json=as_json)


# --------------------------------------------------------------------- 入口
COMMANDS = {
    "version": cmd_version,
    "whoami": cmd_whoami,
    "status": cmd_status,
    "groups": cmd_groups,
    "friends": cmd_friends,
    "members": cmd_members,
    "group-info": cmd_group_info,
    "history": cmd_history,
    "send": cmd_send,
    "call": cmd_call,
    "actions": cmd_actions,
    "doc": cmd_doc,
    "sync-docs": cmd_sync_docs,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    argv, gopts = extract_global(argv)
    if not argv:
        build_parser().print_help()
        return EXIT_OK
    parser = build_parser()
    args = parser.parse_args(argv)
    cfg = config.resolve()
    client = NapCatClient(gopts["base"], gopts["token"], gopts["timeout"])
    try:
        return COMMANDS[args.command](client, args, cfg, gopts["as_json"])
    except NapCatError as exc:
        if gopts["as_json"]:
            _print_json({"ok": False, "error": str(exc), "action": exc.action, "retcode": exc.retcode})
        print(f"[NapCat 错误] {exc}", file=sys.stderr)
        return EXIT_ERROR
    except (FileNotFoundError, ValueError) as exc:
        if gopts["as_json"]:
            _print_json({"ok": False, "error": str(exc)})
        print(f"[参数错误] {exc}", file=sys.stderr)
        return EXIT_ERROR
    except SystemExit as exc:
        # 命令内部用 raise SystemExit("说明") 报参数错误：统一成退出码 2。
        code = exc.code
        if isinstance(code, str):
            if gopts["as_json"]:
                _print_json({"ok": False, "error": code})
            print(f"[参数错误] {code}", file=sys.stderr)
            return EXIT_ERROR
        return int(code or 0)


if __name__ == "__main__":
    raise SystemExit(main())
