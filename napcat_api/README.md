# napcat_api

把 NapCat 的 OneBot 11 HTTP API 封装成命令行工具和 Python 客户端。官方文档里
**204 个 action** 都能通过 `call` 调用，高频操作另有更顺手的快捷命令。

- 零第三方依赖，Python 3.9+。
- 自动读取本地 NapCat 配置里的 HTTP 地址、token、QQ 号和版本。
- 内置官方 OpenAPI 快照（`spec.json`，版本 4.18.42），可一条命令跟进官方文档。
- `--json` 输出，方便 DeepSeek Harness、脚本或其它程序解析。

## 快速开始

```bash
cd D:\DSH_WorkArea

python -m napcat_api version --check   # 环境、账号、NapCat/文档版本一次看全
python -m napcat_api whoami            # 当前登录账号
python -m napcat_api groups            # 群列表
python -m napcat_api call get_status   # 直接调官方 action
python -m napcat_api send -g 123456 -t "你好"
```

`--json` 可以放在任意位置：

```bash
python -m napcat_api whoami --json
python -m napcat_api --json call get_login_info
```

## 环境与配置

默认按以下顺序找 NapCat：`D:\NapCat`、`C:\NapCat`、`~/NapCat`。
找到后扫描 `napcat\config\onebot11_*.json`，取第一个启用的 `httpServers` 条目。

可覆盖的环境变量：

| 变量 | 作用 |
| --- | --- |
| `NAPCAT_ROOT` | NapCat 根目录 |
| `NAPCAT_HTTP` | HTTP 基地址，如 `http://127.0.0.1:3000` |
| `NAPCAT_TOKEN` | OneBot access token |
| `NAPCAT_QQ` | 指定账号（多账号时选配置） |
| `NAPCAT_TIMEOUT` | 请求超时秒数 |
| `NAPCAT_VERSION` | 指定文档版本（默认读 `version.json`） |

命令行也可以临时覆盖：

```bash
python -m napcat_api --base http://127.0.0.1:3000 --token xxx call get_login_info
```

`version.json` 记录本地文档版本与来源（`docs` / `online` / 手工）：

```json
{
  "napcat_version": "4.18.42",
  "qq_version": "9.9.31-49738",
  "source": "docs",
  "updated_at": "2026-11-01T07:00:00+08:00"
}
```

## 命令

| 命令 | 说明 |
| --- | --- |
| `version [--check]` | 本地配置、QQ/NapCat 版本、在线版本、文档版本 |
| `whoami` | 当前登录账号 |
| `status` | NapCat 运行状态 |
| `groups [--no-cache]` | 群列表 |
| `friends` | 好友列表 |
| `members <群号>` | 群成员 |
| `group-info <群号>` | 群信息 |
| `history --group/--user <id> [--count N] [--message-seq N]` | 聊天记录 |
| `send` | 发消息，见下 |
| `call <action>` | 调任意官方 action |
| `actions [--tag 分类] [--search 关键词]` | 列出 action |
| `doc <action>` | 查看 action 参数与示例 |
| `sync-docs [版本] [--check]` | 同步官方 OpenAPI |

### send

```bash
# 群聊
python -m napcat_api send -g 123456 -t "文本" --image D:\pics\a.png --at 10001 --reply 987654321

# 私聊
python -m napcat_api send -u 10001 -t "你好"

# 本地文件会读成 base64；也支持 http(s):// 与 base64://
python -m napcat_api send -g 123456 --file D:\docs\a.pdf

# 只构造请求，不发送（base64 会折叠成 <N chars>）
python -m napcat_api send -g 123456 -t "测试" --image a.png --dry-run
```

`--text`、`--image`、`--record`、`--video`、`--file`、`--at`、`--face` 都可以重复。
`--json-card` 接受 JSON 字符串，`--markdown` 发送 markdown 段。

### call

```bash
python -m napcat_api call get_login_info
python -m napcat_api call get_group_list --json
python -m napcat_api call send_group_msg --params '{"group_id":123456,"message":"hi"}'
python -m napcat_api call set_group_ban -P group_id=123456 -P user_id=10001 -P duration=60
python -m napcat_api call some_new_action --params-file params.json --force
```

- `--params` / `-p`：整个 JSON 对象。
- `--param` / `-P`：单个 `K=V`，值会自动转 bool/int/float/JSON。
- `--params-file`：从 UTF-8 文件读 JSON。
- 参数名不在官方文档里时默认拒绝；`--force` 跳过校验（NapCat 新版本新增的参数会用得上）。

### sync-docs

```bash
python -m napcat_api sync-docs            # 按本地 NapCat 版本同步
python -m napcat_api sync-docs 4.18.42    # 指定版本
python -m napcat_api sync-docs --check    # 只比对版本，不写文件
```

同步过程：读版本列表 → 找到该版本的入口 JS → 从 `chunks/openapi.<hash>.js`
取出 OpenAPI → 裁剪成 `spec.json` → 更新 `version.json`。需要本机有 `node`；
可用 `--node <路径>` 指定。

## Python 客户端

```python
from napcat_api import NapCatClient, text, image, at

client = NapCatClient()                 # 自动读配置
print(client.get_login_info())

client.send_group(123456, [text("你好"), image("D:/pics/a.png"), at(10001)])
client.call("set_group_ban", {"group_id": 123456, "user_id": 10001, "duration": 60})

# 任意 action 也可以直接当方法用
client.get_group_list()
```

底层方法：

- `raw_call(action, params)`：返回完整响应（status/retcode/data）。
- `call(action, params)`：校验并只返回 `data`，失败抛 `NapCatError`。
- `send_group(group_id, message)` / `send_private(user_id, message)` / `send_to("group:123", ...)`。
- `parse_target("group:123")` 解析 `group:` / `user:` / `g:` / `u:` 前缀。

消息段构造器在 `napcat_api.segments`：`text/at/at_all/reply/face/image/record/
video/file/json_card/markdown/forward_id/node/forward_nodes`。

## 版本与文档

`spec.json` 是官方 OpenAPI 的裁剪快照，只保留 action 名、摘要、参数和示例，
不含完整 schema。`doc <action>` 就是从它渲染的。NapCat 升级后跑一次
`sync-docs` 即可对齐；`version --check` 会同时报告本地记录、在线 NapCat 和官方
文档三方版本。

## 退出码

- `0`：成功。
- `2`：参数错误、action 不存在、NapCat 返回失败、网络/鉴权错误。

错误信息写到 stderr，成功结果写到 stdout，方便管道和程序调用。

## 与 DSH 插件的关系

`D:\DSH_WorkArea\napcat-tools` 是它的 Harness 包装：插件把 `napcat_call` /
`napcat_send` 两个模型工具的参数拼成这里的命令行，再解析 `--json` 输出。
Python 包可以完全独立使用，不依赖 DSH。
