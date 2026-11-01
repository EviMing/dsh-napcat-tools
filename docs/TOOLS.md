# DSH 工具参考

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
