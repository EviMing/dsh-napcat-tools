#!/usr/bin/env python3
"""Generate the user-facing API reference from napcat_api/spec.json.

Run from the repository root:

    python tools/gen_docs.py

Outputs:
    docs/ACTIONS.md   204 actions grouped by tag
    docs/QZONE.md     28 Qzone actions + task recipes
    docs/TOOLS.md     DSH tool reference

The official OpenAPI snapshot has a few gaps (no description/example for some
actions).  The generator keeps those gaps visible instead of inventing text.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from napcat_api import spec  # noqa: E402

DOCS = ROOT / "docs"

TAG_ORDER = [
    "核心接口",
    "消息接口",
    "消息扩展",
    "群组接口",
    "群组扩展",
    "用户接口",
    "用户扩展",
    "系统接口",
    "系统扩展",
    "文件接口",
    "文件扩展",
    "流式接口",
    "流式传输扩展",
    "频道接口",
    "扩展接口",
    "QQ空间扩展",
    "AI 扩展",
    "Go-CQHTTP",
]


def one_line(value: object, limit: int = 320) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = text.replace("|", "\\|")
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    return text


def type_name(schema: object) -> str:
    if not isinstance(schema, dict):
        return "任意"
    if "$ref" in schema:
        return str(schema["$ref"]).rsplit("/", 1)[-1]
    for key in ("anyOf", "oneOf"):
        if isinstance(schema.get(key), list):
            names = [type_name(item) for item in schema[key]]
            return " / ".join(dict.fromkeys(names))
    kind = schema.get("type")
    if isinstance(kind, list):
        return "/".join(str(item) for item in kind)
    if kind == "array":
        return f"array<{type_name(schema.get('items'))}>"
    if kind == "object":
        return "object"
    return str(kind or "任意")


def extra_note(schema: object) -> str:
    if not isinstance(schema, dict):
        return ""
    notes: list[str] = []
    if "default" in schema:
        notes.append(f"默认 `{schema['default']}`")
    if isinstance(schema.get("enum"), list) and schema["enum"]:
        values = ", ".join(f"`{item}`" for item in schema["enum"])
        notes.append(f"可选：{values}")
    return "；".join(notes)


def param_table(action: dict) -> list[str]:
    params = action.get("params") or {}
    props = params.get("properties") or {}
    required = set(params.get("required") or [])
    if not props:
        return ["无参数。"]
    lines = [
        "| 参数 | 类型 | 必填 | 说明 |",
        "|---|---|---|---|",
    ]
    for name in props:
        prop = props[name] or {}
        desc = one_line(prop.get("description") or "")
        note = extra_note(prop).replace("|", "\\|")
        if note:
            desc = f"{desc}（{note}）" if desc else note
        lines.append(
            f"| `{name}` | {type_name(prop).replace('|', '\\|')} | {'是' if name in required else '否'} | {desc} |"
        )
    return lines


def example_lines(action: dict) -> list[str]:
    example = action.get("example")
    if example is None or (isinstance(example, (dict, list)) and not example):
        has_params = bool(((action.get("params") or {}).get("properties")))
        if has_params:
            return ["官方未提供示例，请按参数表构造。"]
        return ["官方未提供示例。无参数 action 可直接调用 `{}`。"]
    return [
        "```json",
        json.dumps(example, ensure_ascii=False, indent=2),
        "```",
    ]


def render_action(name: str, action: dict, heading: str = "###") -> list[str]:
    lines = [f"{heading} `{name}`", ""]
    summary = one_line(action.get("summary"))
    if summary:
        lines.append(f"**摘要**：{summary}")
    tags = action.get("tags") or []
    if tags:
        lines.append("**标签**：" + "、".join(f"`{tag}`" for tag in tags))
    if action.get("deprecated"):
        lines += ["", "> ⚠️ 该 action 已被官方标记为 deprecated。"]
    description = str(action.get("description") or "").strip()
    if description:
        lines += ["", "**说明**", "", description]
    lines += ["", "**参数**", ""]
    lines += param_table(action)
    lines += ["", "**示例**", ""]
    lines += example_lines(action)
    lines.append("")
    return lines


def load_actions() -> tuple[dict, dict[str, list[str]]]:
    actions = spec.actions()
    groups: "OrderedDict[str, list[str]]" = OrderedDict((tag, []) for tag in TAG_ORDER)
    for name, action in actions.items():
        tags = action.get("tags") or ["未分类"]
        primary = next((tag for tag in TAG_ORDER if tag in tags), tags[0])
        groups.setdefault(primary, []).append(name)
    for names in groups.values():
        names.sort()
    groups = OrderedDict((tag, names) for tag, names in groups.items() if names)
    return actions, groups


def write_actions() -> None:
    actions, groups = load_actions()
    missing_desc = [name for name, a in actions.items() if not a.get("description")]
    missing_params = [
        name for name, a in actions.items() if not ((a.get("params") or {}).get("properties"))
    ]
    missing_example = [
        name
        for name, a in actions.items()
        if a.get("example") is None
        or (isinstance(a.get("example"), (dict, list)) and not a.get("example"))
    ]

    lines = [
        "# NapCat Action 参考",
        "",
        f"本文件由 `tools/gen_docs.py` 从 `napcat_api/spec.json` 生成，对应官方文档版本 "
        f"**{spec.spec_version()}**，共 **{len(actions)} 个 action**。",
        "",
        "> `spec.json` 是官方 OpenAPI 的裁剪快照；`python -m napcat_api doc <action>` "
        "输出的是同一份数据。NapCat 升级后执行 `python -m napcat_api sync-docs` 更新快照，"
        "再运行本生成器即可刷新此文档。",
        "",
        "## 覆盖情况",
        "",
        f"- 有摘要：{len(actions) - sum(1 for a in actions.values() if not a.get('summary'))} / {len(actions)}",
        f"- 官方未提供详细说明：{len(missing_desc)} 个",
        f"- 没有参数表：{len(missing_params)} 个（多数是本来就没有参数的 action）",
        f"- 官方未提供示例：{len(missing_example)} 个（多数是无参数 action）",
        "",
        "缺失项是官方 OpenAPI 本身的数据缺口，不是封装遗漏；下面按标签分组，"
        "每个 action 的参数和示例均按快照原样渲染。",
        "",
        "## 分类索引",
        "",
    ]
    for index, (tag, names) in enumerate(groups.items(), start=1):
        lines.append(f"- [{tag}](#tag-{index}) — {len(names)} 个")
    lines += [
        "",
        "---",
        "",
    ]
    for index, (tag, names) in enumerate(groups.items(), start=1):
        lines += [f'<a id="tag-{index}"></a>', "", f"## {index}. {tag}（{len(names)}）", ""]
        for name in names:
            lines += render_action(name, actions[name])
    lines += [
        "---",
        "",
        "## 怎么查",
        "",
        "```bash",
        "python -m napcat_api actions --search qzone",
        "python -m napcat_api doc send_group_msg",
        "```",
        "",
    ]
    (DOCS / "ACTIONS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"ACTIONS.md: {len(actions)} actions, {len(groups)} groups")


QZONE_INTRO = """# QQ 空间接口

QQ 空间相关能力来自 NapCat 的 **SnowLuma 扩展**，不在标准 OneBot 11 规范里。
当前快照（4.18.42）共 **28 个 action**：

- **普通空间（14 个）**：看资料/说说/评论、发说说、评论、点赞、删除、权限。
- **空友爱看（14 个）**：另一套公开动态流，操作对象是完整的 `feed` 对象。

这些 action 和普通 action 一样通过 `napcat_call` 调用：

```json
{"action": "get_qzone_msg_list", "params": {"target_uin": "123456789", "num": 5}}
```

```bash
python -m napcat_api call get_qzone_msg_list --params '{"target_uin":"123456789","num":5}' --json
```

> 写操作会真实生效。发说说建议先用 `ugc_right: 64`（仅自己可见）验证。
> 看别人空间受对方权限限制；非好友或不可见时由上游返回错误。

## 普通空间：常用任务

### 看自己的空间

```json
{"action": "get_qzone_profile"}
{"action": "get_qzone_msg_list", "params": {"num": 20}}
```

`get_qzone_msg_list` 返回 `total` 和 `msglist`，每条含 `tid`、`content`、`time`、
`comment_num`、`images`、`is_private`，适合先扫列表再取详情。

### 看别人的空间

```json
{"action": "get_qzone_profile", "params": {"target_uin": "123456789"}}
{"action": "get_qzone_msg_list", "params": {"target_uin": "123456789", "num": 10}}
```

`target_uin` 是空间主人的 QQ 号。资料接口只返回空间名称/说明；说说列表才是内容。

### 看某条说说的详情和评论

```json
{"action": "get_qzone_msg_detail",
 "params": {"target_uin": "123456789", "tid": "d43708d9240ae56ae9670e00", "num": 20}}
```

详情返回 `comments`，每条评论有 `comment_id`、`uin`、`name`、`content`、`replies`。
要翻更多评论时，改用 `get_qzone_comment_list`，它需要 native 模式列表/详情返回的
`feed_ref` 和 `next_cursor`；默认 SnowLuma 详情已经带了首批评论。

### 发说说

```json
{"action": "send_qzone_msg",
 "params": {"content": "今天天气不错", "images": ["file:///D:/pics/a.png"], "ugc_right": 1}}
```

- `content` 必填，纯文本。
- `images` 支持 `file://`、`http(s)://`、`base64://`。通过 `napcat_call` 调用时不会把普通
  本地路径自动转成 base64，本地文件请写成 `file:///D:/pics/a.png` 或先转 `base64://`。
- `ugc_right`：`1` 所有人、`4` 好友、`16` 部分好友可见、`64` 仅自己、`128` 部分好友不可见。
- `16` / `128` 时必须同时给 `target_uins`（QQ 号数组）。

### 评论和回复

一级评论：

```json
{"action": "comment_qzone",
 "params": {"target_uin": "123456789", "tid": "d43708d9240ae56ae9670e00", "content": "确实"}}
```

回复某条评论，带父评论的 `comment_id` 和 `comment_uin`：

```json
{"action": "comment_qzone",
 "params": {"target_uin": "123456789", "tid": "d43708d9240ae56ae9670e00",
            "content": "回复你", "comment_id": "1", "comment_uin": "10001"}}
```

指定被回复人时再加 `reply_uin` / `reply_name`；楼中楼只支持文字，一级评论可用
`images` 传图。

### 点赞 / 取消赞

```json
{"action": "like_qzone",
 "params": {"target_uin": "123456789", "tid": "d43708d9240ae56ae9670e00", "abstime": 0}}
```

`abstime` 是说说的发布时间戳，不知道就传 `0`；取消赞把 action 换成 `unlike_qzone`，
参数相同。

### 删除、权限、访问限制

```json
{"action": "delete_qzone_msg", "params": {"tid": "d43708d9240ae56ae9670e00"}}
{"action": "set_qzone_msg_right",
 "params": {"tid": "d43708d9240ae56ae9670e00", "ugc_right": 64}}
{"action": "set_qzone_ban", "params": {"user_id": "10001", "enable": true}}
```

`delete_qzone_msg` 按 tid 删除自己的说说（权限由上游校验）；`set_qzone_msg_right` 只能改自己的；
`set_qzone_ban` 是设置别人访问自己空间的限制，`enable:false` 取消。

## 普通空间：全部 14 个 action
"""

QZONE_PUBLIC_INTRO = """## 空友爱看：另一套公开动态

这 14 个 action 操作的不是普通说说，而是“空友爱看”的 `feed` 对象。必须先通过
`get_qzone_public_feeds`（或详情）拿到**完整 feed 对象**，后续操作原样传回；
不要自己拼字段。翻页用返回的 `next_cursor` / `attach_info`。

```json
{"action": "get_qzone_public_feeds"}
{"action": "set_qzone_public_like", "params": {"feed": { ...完整对象... }, "enable": true}}
```

这条链路有两个独立的“赞”：`set_qzone_public_like` 是普通赞，
`set_qzone_public_upvote` 是“推”，`set_qzone_public_follow` 是“蹲作者”，
`set_qzone_public_comment_like` 是评论/回复赞，互不替代。

## 空友爱看：全部 14 个 action
"""


def write_qzone() -> None:
    actions = spec.actions()
    qzone = [name for name in actions if "qzone" in name]
    ordinary = [name for name in qzone if "QQ空间扩展" not in (actions[name].get("tags") or [])]
    public = [name for name in qzone if "QQ空间扩展" in (actions[name].get("tags") or [])]
    ordinary.sort()
    public.sort()

    lines = [QZONE_INTRO, ""]
    for name in ordinary:
        lines += render_action(name, actions[name])
    lines += [QZONE_PUBLIC_INTRO, ""]
    for name in public:
        lines += render_action(name, actions[name])
    lines += [
        "---",
        "",
        "## 注意",
        "",
        "- `tid` 与 `feed_ref` 是两种互斥的定位方式，不能混用。",
        "- `pos`/`num` 与 `cursor` 也不能混用；native 模式不接受 `page_num`/`count`。",
        "- 返回里的 `html` 字段可能非常大，程序化处理时优先取 `content`、`tid`、"
        "`comments` 等结构化字段。",
        "- 写操作没有二次确认，调用前确认 `target_uin`、`tid` 和权限参数。",
        "",
    ]
    (DOCS / "QZONE.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"QZONE.md: {len(ordinary)} ordinary + {len(public)} public actions")


TOOLS_MD = """# DSH 工具参考

本仓库的 Host 插件注册两个模型工具。工具只负责拼参数并启动
`python -m napcat_api`，协议细节都在 Python 包里。

## `napcat_call`

调用 NapCat/OneBot 11 的任意 action。当前文档 4.18.42 共 204 个。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `action` | string | 是 | action 名，如 `get_login_info`、`send_group_msg`、`get_qzone_msg_list` |
| `params` | object | 否 | 传给该 action 的 JSON 参数对象；默认 `{}` |
| `force` | boolean | 否 | 参数不在本地 spec 中时仍强制发送，默认 `false` |

### 返回

成功：

```json
{"ok": true, "action": "get_login_info", "data": {"user_id": 3641194452, "nickname": "大肥鱼"}}
```

失败时工具抛错，DSH 会显示错误文本；`napcat_api` 的退出码、stderr 摘要会包含在错误里。

### 示例

```json
{"action": "get_login_info"}
{"action": "get_group_list"}
{"action": "send_group_msg", "params": {"group_id": 123456, "message": "hello"}}
{"action": "set_group_ban", "params": {"group_id": 123456, "user_id": 10001, "duration": 60}}
```

`force` 只跳过本地参数名校验，不能绕过 NapCat 自身的校验：

```json
{"action": "some_new_action", "params": {"foo": "bar"}, "force": true}
```

> ⚠️ 不做业务风控：`set_group_ban`、`set_group_kick`、退群等管理操作会直接执行。

## `napcat_send`

`send_group_msg` / `send_private_msg` 的快捷封装，适合只发消息、不想手写消息段数组的场景。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `target` | string | 是 | `group:群号` 或 `user:QQ号`；也接受 `g:`、`u:`、`private:`、`p:` |
| `text` | string | 否 | 文本内容 |
| `images` | string[] | 否 | 图片：本地路径、`http(s)://`、`base64://` |
| `files` | string[] | 否 | 文件：本地路径、`http(s)://`、`base64://` |
| `at` | string[] | 否 | 要 @ 的 QQ 号；`all` 表示全体成员 |
| `reply` | string | 否 | 引用消息的 `message_id` |
| `record` | string | 否 | 语音：本地路径、URL 或 `base64://` |
| `video` | string | 否 | 视频：本地路径、URL 或 `base64://` |
| `face` | string[] | 否 | QQ 表情 id |
| `markdown` | string | 否 | Markdown 内容（NapCat 支持的场景） |
| `jsonCard` | string | 否 | JSON 卡片内容（JSON 字符串） |
| `dryRun` | boolean | 否 | 只构造请求并返回，不真正发送，默认 `false` |

`text`、`images`、`files`、`at`、`record`、`video`、`face`、`markdown`、`jsonCard`
可以任意组合；本地媒体由 Python 侧读取并转成 `base64://`。

### 返回

```json
{"ok": true, "action": "send_group_msg", "data": {"message_id": 123456789}}
```

`dryRun: true` 时额外带 `"dryRun": true`，`data` 是构造出的请求参数，不会发送。

### 示例

```json
{"target": "group:123456", "text": "晚上好", "at": ["10001"]}
{"target": "user:10001", "text": "看图", "images": ["D:/pics/a.png"]}
{"target": "group:123456", "text": "回复你", "reply": "123456789"}
{"target": "group:123456", "text": "测试", "dryRun": true}
```

`target` 必须带前缀；只写数字会报错。`reply` 是消息 id，不是 QQ 号。

## 插件配置

| 键 | 默认 | 说明 |
|---|---|---|
| `cwd` | 安装时配置 | `napcat_api` 包所在目录；Python 以它为工作目录 |
| `python` | 空 | 空则依次尝试 `python`、`py`；也可填绝对路径 |
| `pythonPath` | 空 | 额外的 `PYTHONPATH` |
| `timeoutMs` | `120000` | 单次调用超时（毫秒） |
| `enabled` | `true` | 设为 `false` 可停用插件 |

NapCat 的 HTTP 地址和 token 不在插件配置里：Python 包会读取
`<NapCat>/napcat/config/onebot11_*.json` 中启用的 `httpServers`，也支持
`NAPCAT_HTTP` / `NAPCAT_TOKEN` 环境变量。

## 相关文档

- [204 个 action 参考](ACTIONS.md)
- [QQ 空间 28 个接口](QZONE.md)
- [Python CLI 与客户端](../napcat_api/README.md)
"""


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    write_actions()
    write_qzone()
    (DOCS / "TOOLS.md").write_text(TOOLS_MD, encoding="utf-8")
    print("TOOLS.md")


if __name__ == "__main__":
    main()
