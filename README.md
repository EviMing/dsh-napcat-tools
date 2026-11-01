# dsh-napcat-tools

把本地 [NapCat](https://napneko.github.io/) 的 OneBot 11 HTTP API 封装成：

1. **DeepSeek Harness Host 插件**：提供 `napcat_call` / `napcat_send` 两个模型工具；
2. **零依赖 Python CLI**：`python -m napcat_api`，覆盖官方文档 4.18.42 的 **204 个 action**。

插件本身不实现 QQ 协议，只负责拼参数、启动本仓库里的 Python 包，并把 `--json`
结果交回 Harness。Python 包可以完全独立使用，不依赖 DSH。

## 仓库结构

```text
.
├── index.js              # DSH Host 插件入口，注册两个工具
├── lib/runner.mjs        # spawn python -m napcat_api，收集并解析 JSON
├── package.json          # DSH bundle 清单
├── cordis.patch.yml      # 安装时插入的插件配置
├── docs/                 # 完整文档
│   ├── ACTIONS.md        # 204 个 action 参考（生成）
│   ├── QZONE.md          # 28 个 QQ 空间接口（生成）
│   └── TOOLS.md          # DSH 工具参考
├── tools/gen_docs.py     # 从 spec 重新生成文档
└── napcat_api/           # Python 包（CLI + 客户端 + 官方 spec 快照）
    ├── cli.py
    ├── client.py
    ├── config.py
    ├── segments.py
    ├── spec.py
    ├── sync_docs.py
    ├── spec.json         # 4.18.42 的 204 个 action 裁剪快照
    └── version.json      # 本地记录的文档/版本号
```

## 文档

- [DSH 工具参考](docs/TOOLS.md)：`napcat_call` / `napcat_send` 的全部参数、返回值和示例。
- [204 个 action 参考](docs/ACTIONS.md)：按标签分组，含参数表、官方示例和覆盖缺口。
- [QQ 空间 28 个接口](docs/QZONE.md)：看空间、发说说、评论、点赞、权限与“空友爱看”。

`docs/` 里的 action 参考由 `tools/gen_docs.py` 从 `napcat_api/spec.json` 生成；
NapCat 升级后先 `python -m napcat_api sync-docs`，再运行生成器：

```bash
python tools/gen_docs.py
```

## 前置条件

- Windows 上的 NapCat，已登录并启用 OneBot 11 HTTP 服务（默认 `127.0.0.1:3000`）。
- Python 3.9+，不需要第三方包。
- 可选：Node.js，仅 `sync-docs` 解析官方 OpenAPI 分块时需要。
- DeepSeek Harness，且本机 profile 可安装 Host 插件。

NapCat 的地址、token、QQ 号由 Python 包自动发现：扫描
`<NapCat>/napcat/config/onebot11_*.json` 里启用的 `httpServers`。也可以用环境变量
`NAPCAT_ROOT` / `NAPCAT_HTTP` / `NAPCAT_TOKEN` / `NAPCAT_QQ` 覆盖。

## 安装

### 1. 放置仓库

```bash
git clone https://github.com/EviMing/dsh-napcat-tools.git
cd dsh-napcat-tools
```

### 2. 验证 Python CLI

```bash
python -m napcat_api version --check
python -m napcat_api whoami
```

看到 `NapCat 版本 / 文档版本 / 在线探测` 就说明配置正确。更多命令见
[napcat_api/README.md](napcat_api/README.md)。

### 3. 安装 DSH 插件

把 `cordis.patch.yml` 里的 `cwd` 改成**本仓库根目录**：

```yaml
config:
  cwd: 'D:\path\to\dsh-napcat-tools'
  python: ''
  timeoutMs: 120000
```

然后：

```text
plugin_manager action=install_bundle target=D:\path\to\dsh-napcat-tools
```

新安装的 bundle 立即生效；之后修改 `index.js` 需要重启 DSH 才会重新加载。

## 工具

### `napcat_call`

调用任意官方 action：

```json
{ "action": "get_login_info" }
{ "action": "get_group_info", "params": { "group_id": 1103136906 } }
{ "action": "send_group_msg", "params": { "group_id": 1103136906, "message": "hello" } }
```

返回 `{ ok, action, data }`。参数名不在官方文档里时默认拒绝，加 `"force": true` 跳过校验。

### `napcat_send`

群聊/私聊快捷发送：

```json
{ "target": "group:1103136906", "text": "晚上好", "at": ["10001"] }
{ "target": "user:10001", "text": "看图", "images": ["D:\\pics\\a.png"] }
{ "target": "group:1103136906", "text": "回复你", "reply": "123456789" }
```

支持 `text` / `images` / `files` / `at` / `reply` / `record` / `video` / `face` /
`markdown` / `jsonCard` / `dryRun`。本地媒体由 Python 侧读成 `base64://`，也可以直接给
`http(s)://` 或 `base64://`。

## Python CLI 速查

```bash
python -m napcat_api version --check    # 环境/账号/版本
python -m napcat_api whoami
python -m napcat_api groups
python -m napcat_api history -g 1103136906 -n 20
python -m napcat_api send -g 1103136906 -t "你好" --image D:\pics\a.png
python -m napcat_api call get_group_list --json
python -m napcat_api actions --search group
python -m napcat_api doc send_group_msg
python -m napcat_api sync-docs          # 按官方 /api/<版本> 更新 spec.json
```

完整参数见 [napcat_api/README.md](napcat_api/README.md)。

## 版本与文档

- `napcat_api/version.json` 记录上次同步的 NapCat/文档版本；
- `python -m napcat_api sync-docs` 按官方 `https://napneko.github.io/api/<版本>`
  重新抓取 OpenAPI，写入 `spec.json`；
- `version --check` 同时显示本地记录、在线 NapCat、官方文档三方版本。

## 安全提示

- `napcat_call` 不做业务风控：`set_group_ban`、`set_group_kick`、退群等操作会直接执行。
- NapCat 的 access token 只存在于本地配置文件，本仓库不包含任何 token 或账号密码。
- 建议只在本机或可信网络暴露 OneBot HTTP 端口。

## License

MIT
