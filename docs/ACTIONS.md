# NapCat Action 参考

本文件由 `tools/gen_docs.py` 从 `napcat_api/spec.json` 生成，对应官方文档版本 **4.18.42**，共 **204 个 action**。

> `spec.json` 是官方 OpenAPI 的裁剪快照；`python -m napcat_api doc <action>` 输出的是同一份数据。NapCat 升级后执行 `python -m napcat_api sync-docs` 更新快照，再运行本生成器即可刷新此文档。

## 覆盖情况

- 有摘要：204 / 204
- 官方未提供详细说明：63 个
- 没有参数表：27 个（多数是本来就没有参数的 action）
- 官方未提供示例：26 个（多数是无参数 action）

缺失项是官方 OpenAPI 本身的数据缺口，不是封装遗漏；下面按标签分组，每个 action 的参数和示例均按快照原样渲染。

## 分类索引

- [核心接口](#tag-1) — 6 个
- [消息接口](#tag-2) — 10 个
- [消息扩展](#tag-3) — 9 个
- [群组接口](#tag-4) — 25 个
- [群组扩展](#tag-5) — 18 个
- [用户接口](#tag-6) — 6 个
- [用户扩展](#tag-7) — 4 个
- [系统接口](#tag-8) — 13 个
- [系统扩展](#tag-9) — 16 个
- [文件接口](#tag-10) — 5 个
- [文件扩展](#tag-11) — 17 个
- [流式接口](#tag-12) — 2 个
- [流式传输扩展](#tag-13) — 4 个
- [频道接口](#tag-14) — 2 个
- [扩展接口](#tag-15) — 24 个
- [QQ空间扩展](#tag-16) — 14 个
- [AI 扩展](#tag-17) — 2 个
- [Go-CQHTTP](#tag-18) — 27 个

---

<a id="tag-1"></a>

## 1. 核心接口（6）

### `cancel_group_todo`

**摘要**：取消群待办
**标签**：`核心接口`

**说明**

将指定消息对应的群待办取消

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string / number | 是 | 群号 |
| `message_id` | string | 否 | 消息ID |
| `message_seq` | string | 否 | 消息Seq (可选) |

**示例**

```json
{
  "group_id": "123456",
  "message_id": "123456789"
}
```

### `complete_group_todo`

**摘要**：完成群待办
**标签**：`核心接口`

**说明**

将指定消息对应的群待办标记为已完成

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string / number | 是 | 群号 |
| `message_id` | string | 否 | 消息ID |
| `message_seq` | string | 否 | 消息Seq (可选) |

**示例**

```json
{
  "group_id": "123456",
  "message_id": "123456789"
}
```

### `friend_poke`

**摘要**：发送戳一戳
**标签**：`核心接口`

**说明**

在群聊或私聊中发送戳一戳动作

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 否 | 群号 |
| `user_id` | string | 是 | 用户QQ |
| `target_id` | string | 否 | 目标QQ |

**示例**

```json
{
  "user_id": "123456789"
}
```

### `group_poke`

**摘要**：发送戳一戳
**标签**：`核心接口`

**说明**

在群聊或私聊中发送戳一戳动作

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 否 | 群号 |
| `user_id` | string | 是 | 用户QQ |
| `target_id` | string | 否 | 目标QQ |

**示例**

```json
{
  "user_id": "123456789"
}
```

### `send_poke`

**摘要**：发送戳一戳
**标签**：`核心接口`

**说明**

在群聊或私聊中发送戳一戳动作

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 否 | 群号 |
| `user_id` | string | 是 | 用户QQ |
| `target_id` | string | 否 | 目标QQ |

**示例**

```json
{
  "user_id": "123456789"
}
```

### `set_group_todo`

**摘要**：设置群待办
**标签**：`核心接口`

**说明**

将指定消息设置为群待办

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string / number | 是 | 群号 |
| `message_id` | string | 否 | 消息ID |
| `message_seq` | string | 否 | 消息Seq (可选) |

**示例**

```json
{
  "group_id": "123456",
  "message_id": "123456789"
}
```

<a id="tag-2"></a>

## 2. 消息接口（10）

### `_mark_all_as_read`

**摘要**：标记所有消息已读
**标签**：`消息接口`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `delete_msg`

**摘要**：撤回消息
**标签**：`消息接口`

**说明**

撤回已发送的消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |

**示例**

```json
{
  "message_id": 12345
}
```

### `forward_friend_single_msg`

**摘要**：转发单条消息
**标签**：`消息接口`

**说明**

转发单条消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |
| `group_id` | string | 否 | 目标群号 |
| `user_id` | string | 否 | 目标用户QQ |

**示例**

```json
{
  "message_id": 12345,
  "group_id": "123456"
}
```

### `forward_group_single_msg`

**摘要**：转发单条消息
**标签**：`消息接口`

**说明**

转发单条消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |
| `group_id` | string | 否 | 目标群号 |
| `user_id` | string | 否 | 目标用户QQ |

**示例**

```json
{
  "message_id": 12345,
  "group_id": "123456"
}
```

### `get_msg`

**摘要**：获取消息
**标签**：`消息接口`

**说明**

根据消息 ID 获取消息详细信息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |

**示例**

```json
{
  "message_id": 123456
}
```

### `mark_group_msg_as_read`

**摘要**：标记群聊已读
**标签**：`消息接口`

**说明**

标记指定渠道的消息为已读

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string / number | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message_id` | string | 否 | 消息ID |

**示例**

```json
{
  "message_id": 12345
}
```

### `mark_msg_as_read`

**摘要**：标记消息已读 (Go-CQHTTP)
**标签**：`消息接口`

**说明**

标记指定渠道的消息为已读

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string / number | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message_id` | string | 否 | 消息ID |

**示例**

```json
{
  "message_id": 12345
}
```

### `mark_private_msg_as_read`

**摘要**：标记私聊已读
**标签**：`消息接口`

**说明**

标记指定渠道的消息为已读

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string / number | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message_id` | string | 否 | 消息ID |

**示例**

```json
{
  "message_id": 12345
}
```

### `send_msg`

**摘要**：发送消息
**标签**：`消息接口`

**说明**

发送私聊或群聊消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_type` | string | 否 | 消息类型 (private/group)（可选：`private`, `group`） |
| `user_id` | string | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message` | OB11MessageMixType | 是 |  |
| `auto_escape` | boolean / string | 否 | 是否作为纯文本发送 |
| `source` | string | 否 | 合并转发来源 |
| `news` | array<object> | 否 | 合并转发新闻 |
| `summary` | string | 否 | 合并转发摘要 |
| `prompt` | string | 否 | 合并转发提示 |
| `timeout` | number | 否 | 自定义发送超时(毫秒)，覆盖自动计算值 |

**示例**

```json
{
  "message_type": "group",
  "group_id": "123456",
  "message": "hello"
}
```

### `send_private_msg`

**摘要**：发送私聊消息
**标签**：`消息接口`

**说明**

发送私聊消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_type` | string | 否 | 消息类型 (private/group)（可选：`private`, `group`） |
| `user_id` | string | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message` | OB11MessageMixType | 是 |  |
| `auto_escape` | boolean / string | 否 | 是否作为纯文本发送 |
| `source` | string | 否 | 合并转发来源 |
| `news` | array<object> | 否 | 合并转发新闻 |
| `summary` | string | 否 | 合并转发摘要 |
| `prompt` | string | 否 | 合并转发提示 |
| `timeout` | number | 否 | 自定义发送超时(毫秒)，覆盖自动计算值 |

**示例**

```json
{
  "user_id": "123456789",
  "message": "hello"
}
```

<a id="tag-3"></a>

## 3. 消息扩展（9）

### `ArkShareGroup`

**摘要**：分享群 (Ark)
**标签**：`消息扩展`

**说明**

获取群分享的 Ark 内容

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `ArkSharePeer`

**摘要**：分享用户 (Ark)
**标签**：`消息扩展`

**说明**

获取用户推荐的 Ark 内容

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 否 | QQ号 |
| `group_id` | string | 否 | 群号 |
| `phone_number` | string | 是 | 手机号（默认 ``） |

**示例**

```json
{
  "user_id": "123456",
  "phone_number": ""
}
```

### `click_inline_keyboard_button`

**摘要**：点击内联键盘按钮
**标签**：`消息扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `bot_appid` | string | 是 | 机器人AppID |
| `button_id` | string | 是 | 按钮ID（默认 ``） |
| `callback_data` | string | 是 | 回调数据（默认 ``） |
| `msg_seq` | string | 是 | 消息序列号（默认 `10086`） |

**示例**

```json
{
  "group_id": "123456",
  "bot_appid": "1234567890",
  "button_id": "btn_1",
  "callback_data": "",
  "msg_seq": "10086"
}
```

### `fetch_emoji_like`

**摘要**：获取表情点赞详情
**标签**：`消息扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |
| `emojiId` | number / string | 是 | 表情ID |
| `emojiType` | number / string | 是 | 表情类型 |
| `count` | number / string | 是 | 获取数量（默认 `20`） |
| `cookie` | string | 是 | 分页Cookie（默认 ``） |

**示例**

```json
{
  "message_id": 12345,
  "emojiId": "123",
  "emojiType": 1,
  "count": 10,
  "cookie": ""
}
```

### `fetch_ptt_text`

**摘要**：获取语音转文字结果
**标签**：`消息扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |

**示例**

```json
{
  "message_id": 123456
}
```

### `get_emoji_likes`

**摘要**：获取消息表情点赞列表
**标签**：`消息扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 否 | 群号，短ID可不传 |
| `message_id` | string | 是 | 消息ID，可以传递长ID或短ID |
| `emoji_id` | string | 是 | 表情ID |
| `emoji_type` | string | 否 | 表情类型 |
| `count` | number | 是 | 数量，0代表全部（默认 `0`） |

**示例**

```json
{
  "message_id": "12345",
  "emoji_id": "123"
}
```

### `send_ark_share`

**摘要**：分享用户 (Ark)
**标签**：`消息扩展`

**说明**

获取用户推荐的 Ark 内容

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 否 | QQ号 |
| `group_id` | string | 否 | 群号 |
| `phone_number` | string | 是 | 手机号（默认 ``） |

**示例**

```json
{
  "user_id": "123456",
  "phone_number": ""
}
```

### `send_group_ark_share`

**摘要**：分享群 (Ark)
**标签**：`消息扩展`

**说明**

获取群分享的 Ark 内容

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `set_msg_emoji_like`

**摘要**：设置消息表情点赞
**标签**：`消息扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |
| `emoji_id` | number / string | 是 | 表情ID |
| `set` | boolean / string | 否 | 是否设置 |

**示例**

```json
{
  "message_id": 12345,
  "emoji_id": "123",
  "set": true
}
```

<a id="tag-4"></a>

## 4. 群组接口（25）

### `_del_group_notice`

**摘要**：删除群公告
**标签**：`群组接口`

**说明**

删除群聊中的公告

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `notice_id` | string | 是 | 公告ID |

**示例**

```json
{
  "group_id": "123456",
  "notice_id": "notice_123"
}
```

### `_get_group_notice`

**摘要**：获取群公告
**标签**：`群组接口`

**说明**

获取指定群聊中的公告列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `delete_essence_msg`

**摘要**：移出精华消息
**标签**：`群组接口`

**说明**

将一条消息从群精华消息列表中移出

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 否 | 消息ID |
| `msg_seq` | string | 否 | 消息序号 |
| `msg_random` | string | 否 | 消息随机数 |
| `group_id` | string | 否 | 群号 |

**示例**

```json
{
  "message_id": 123456
}
```

### `get_essence_msg_list`

**摘要**：获取群精华消息
**标签**：`群组接口`

**说明**

获取指定群聊中的精华消息列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_group_detail_info`

**摘要**：获取群详细信息
**标签**：`群组接口`

**说明**

获取群聊的详细信息，包括成员数、最大成员数等

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_group_ignore_add_request`

**摘要**：获取群被忽略的加群请求
**标签**：`群组接口`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_group_ignored_notifies`

**摘要**：获取群忽略通知
**标签**：`群组接口`

**说明**

获取被忽略的入群申请和邀请通知

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_group_info`

**摘要**：获取群信息
**标签**：`群组接口`

**说明**

获取群聊的基本信息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_group_list`

**摘要**：获取群列表
**标签**：`群组接口`

**说明**

获取当前帐号的群聊列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `no_cache` | boolean / string | 否 | 是否不使用缓存 |

**示例**

官方未提供示例，请按参数表构造。

### `get_group_member_info`

**摘要**：获取群成员信息
**标签**：`群组接口`

**说明**

获取群聊中指定成员的信息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `user_id` | string | 是 | QQ号 |
| `no_cache` | boolean / string | 否 | 是否不使用缓存 |

**示例**

```json
{
  "group_id": "123456",
  "user_id": "123456789"
}
```

### `get_group_member_list`

**摘要**：获取群成员列表
**标签**：`群组接口`

**说明**

获取群聊中的所有成员列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `no_cache` | boolean / string | 否 | 是否不使用缓存 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_group_shut_list`

**摘要**：获取群禁言列表
**标签**：`群组接口`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456789"
}
```

### `send_group_msg`

**摘要**：发送群消息
**标签**：`群组接口`

**说明**

发送群消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_type` | string | 否 | 消息类型 (private/group)（可选：`private`, `group`） |
| `user_id` | string | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message` | OB11MessageMixType | 是 |  |
| `auto_escape` | boolean / string | 否 | 是否作为纯文本发送 |
| `source` | string | 否 | 合并转发来源 |
| `news` | array<object> | 否 | 合并转发新闻 |
| `summary` | string | 否 | 合并转发摘要 |
| `prompt` | string | 否 | 合并转发提示 |
| `timeout` | number | 否 | 自定义发送超时(毫秒)，覆盖自动计算值 |

**示例**

```json
{
  "group_id": "123456",
  "message": "hello"
}
```

### `set_essence_msg`

**摘要**：设置精华消息
**标签**：`群组接口`

**说明**

将一条消息设置为群精华消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | number / string | 是 | 消息ID |

**示例**

```json
{
  "message_id": 123456
}
```

### `set_group_add_request`

**摘要**：处理加群请求
**标签**：`群组接口`

**说明**

同意或拒绝加群请求或邀请

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `flag` | string | 是 | 请求flag |
| `approve` | boolean / string | 否 | 是否同意 |
| `reason` | string / null | 否 | 拒绝理由 |
| `count` | number | 否 | 搜索通知数量（默认 `100`） |

**示例**

```json
{
  "flag": "flag_123",
  "sub_type": "add",
  "approve": true
}
```

### `set_group_admin`

**摘要**：设置群管理员
**标签**：`群组接口`

**说明**

设置或取消群聊中的管理员

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `user_id` | string | 是 | 用户QQ |
| `enable` | boolean / string | 否 | 是否设置为管理员 |

**示例**

```json
{
  "group_id": "123456",
  "user_id": "123456789",
  "enable": true
}
```

### `set_group_ban`

**摘要**：群组禁言
**标签**：`群组接口`

**说明**

禁言群聊中的指定成员

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `user_id` | string | 是 | 用户QQ |
| `duration` | number / string | 是 | 禁言时长(秒)（默认 `0`） |

**示例**

```json
{
  "group_id": "123456",
  "user_id": "123456789",
  "duration": 1800
}
```

### `set_group_card`

**摘要**：设置群名片
**标签**：`群组接口`

**说明**

设置群聊中指定成员的群名片

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `user_id` | string | 是 | 用户QQ |
| `card` | string | 否 | 群名片 |

**示例**

```json
{
  "group_id": "123456",
  "user_id": "123456789",
  "card": "新名片"
}
```

### `set_group_kick`

**摘要**：群组踢人
**标签**：`群组接口`

**说明**

将指定成员踢出群聊

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `user_id` | string | 是 | 用户QQ |
| `reject_add_request` | boolean / string | 否 | 是否拒绝加群请求 |

**示例**

```json
{
  "group_id": "123456",
  "user_id": "123456789",
  "reject_add_request": false
}
```

### `set_group_leave`

**摘要**：退出群组
**标签**：`群组接口`

**说明**

退出或解散指定群聊

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `is_dismiss` | boolean / string | 否 | 是否解散 |

**示例**

```json
{
  "group_id": "123456",
  "is_dismiss": false
}
```

### `set_group_member_invite_policy`

**摘要**：设置群成员邀请策略
**标签**：`群组接口`

**说明**

设置是否允许群成员邀请好友进群，以及邀请是否需要管理员审核

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `policy` | string | 是 | 成员邀请策略：禁止、需要管理员审核、无需审核、群成员少于100人时无需审核（可选：`disabled`, `require_approval`, `no_approval`, `no_approval_under_100`） |

**示例**

```json
{
  "group_id": "123456",
  "policy": "require_approval"
}
```

### `set_group_member_permissions`

**摘要**：设置群成员功能权限
**标签**：`群组接口`

**说明**

设置群成员上传相册、发起临时会话和发起新群聊的权限；未传入的项目保持不变

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `allow_member_upload_album` | boolean | 否 | 允许成员上传群相册 |
| `allow_member_temporary_session` | boolean | 否 | 允许成员发起临时会话 |
| `allow_member_create_group` | boolean | 否 | 允许成员发起新的群聊 |

**示例**

```json
{
  "group_id": "123456",
  "allow_member_upload_album": true,
  "allow_member_temporary_session": true,
  "allow_member_create_group": true
}
```

### `set_group_name`

**摘要**：设置群名称
**标签**：`群组接口`

**说明**

修改指定群聊的名称

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `group_name` | string | 是 | 群名称 |

**示例**

```json
{
  "group_id": "123456",
  "group_name": "新群名"
}
```

### `set_group_new_member_history_visibility`

**摘要**：设置新成员历史消息可见性
**标签**：`群组接口`

**说明**

设置新入群成员默认是否可以查看最近聊天记录

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `visible` | boolean | 是 | 新成员默认可见最近聊天记录 |

**示例**

```json
{
  "group_id": "123456",
  "visible": true
}
```

### `set_group_whole_ban`

**摘要**：全员禁言
**标签**：`群组接口`

**说明**

开启或关闭指定群聊的全员禁言

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `enable` | boolean / string | 否 | 是否开启全员禁言 |

**示例**

```json
{
  "group_id": "123456",
  "enable": true
}
```

<a id="tag-5"></a>

## 5. 群组扩展（18）

### `cancel_group_album_media_like`

**摘要**：取消点赞群相册媒体
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册ID |
| `batch_id` | string | 是 | batch_id |
| `lloc` | string | 否 | lloc，若对整个上传操作则不填 |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id",
  "batch_id": "112233",
  "lloc": "aabbcc"
}
```

### `del_group_album_media`

**摘要**：删除群相册媒体
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册ID |
| `lloc` | string | 是 | 媒体ID (lloc) |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id_1",
  "lloc": "media_id_1"
}
```

### `do_group_album_comment`

**摘要**：发表群相册评论
**标签**：`群组扩展`

**说明**

lloc 与 batch_id 至少提供一项。传入 lloc 时评论单张图片；仅传 batch_id 时评论整个上传批次。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册 ID |
| `lloc` | string | 否 | 图片 ID；不传或为空时评论整个上传批次，此时必须提供 batch_id |
| `batch_id` | string | 否 | 上传批次 ID，可取自 get_group_album_media_list 返回的 batch.link_id 或 media[].batch_id |
| `content` | string | 是 | 评论内容 |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id_1",
  "batch_id": "2147483658",
  "content": "很有意思"
}
```

### `get_group_album_media_list`

**摘要**：获取群相册媒体列表
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册ID |
| `attach_info` | string | 否 | 附加信息（用于分页）（默认 ``） |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id_1"
}
```

### `get_group_info_ex`

**摘要**：获取群详细信息 (扩展)
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_group_share_link`

**摘要**：获取群分享链接
**标签**：`群组扩展`

**说明**

通过 NTQQ 原生 getJoinGroupLink 获取群的 H5 分享/加群链接 (qm.qq.com/q/xxx 或 qun.qq.com/universal-share/share?...)

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | number / string | 是 | 群号 |
| `need_short_url` | boolean / string | 否 | 是否返回短链 (qm.qq.com/q/xxx)，false 返回完整 universal-share 链接（默认 `True`） |
| `src_id` | number / string | 否 | 分享来源 ID（默认 `73`） |
| `additional_param` | string | 否 | 附加参数（默认 ``） |

**示例**

```json
{
  "group_id": "123456",
  "need_short_url": true
}
```

### `get_group_signed_list`

**摘要**：获取群组今日打卡列表
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string / number | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_qun_album_list`

**摘要**：获取群相册列表
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `attach_info` | string | 否 | 附加信息（用于分页，从上一次返回结果中获取）（默认 ``） |

**示例**

```json
{
  "group_id": "123456",
  "attach_info": ""
}
```

### `send_group_sign`

**摘要**：群打卡
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456789"
}
```

### `set_group_add_option`

**摘要**：设置群加群选项
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `add_type` | number | 是 | 加群方式 |
| `group_question` | string | 否 | 加群问题 |
| `group_answer` | string | 否 | 加群答案 |

**示例**

```json
{
  "group_id": "123456",
  "add_type": 1
}
```

### `set_group_album_media_like`

**摘要**：点赞群相册媒体
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册ID |
| `batch_id` | string | 是 | batch_id |
| `lloc` | string | 否 | lloc，若对整个上传操作则不填 |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id_123",
  "batch_id": "112233",
  "lloc": "aabbcc12213123"
}
```

### `set_group_remark`

**摘要**：设置群备注
**标签**：`群组扩展`

**说明**

设置群备注

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `remark` | string | 是 | 备注 |

**示例**

```json
{
  "group_id": "123456",
  "remark": "测试群备注"
}
```

### `set_group_robot_add_option`

**摘要**：设置群机器人加群选项
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `robot_member_switch` | number | 否 | 机器人成员开关 |
| `robot_member_examine` | number | 否 | 机器人成员审核 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `set_group_search`

**摘要**：设置群搜索选项
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `no_code_finger_open` | number | 否 | 未知 |
| `no_finger_open` | number | 否 | 未知 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `set_group_sign`

**摘要**：群打卡
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456789"
}
```

### `upload_image_to_qun_album`

**摘要**：上传图片到群相册
**标签**：`群组扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册ID |
| `album_name` | string | 是 | 相册名称 |
| `file` | string | 是 | 图片路径、URL或Base64 |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id_1",
  "album_name": "相册1",
  "file": "/path/to/image.jpg"
}
```

### `upload_images_to_qun_album`

**摘要**：上传多张图片到群相册
**标签**：`群组扩展`

**说明**

一次上传多张图片，这些图片在群相册里显示为同一条上传

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册ID |
| `album_name` | string | 是 | 相册名称 |
| `files` | array<string> | 是 | 图片路径、URL或Base64 数组，一次上传多张 |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id_1",
  "album_name": "相册1",
  "files": [
    "/path/to/1.jpg",
    "/path/to/2.jpg"
  ]
}
```

### `upload_video_to_qun_album`

**摘要**：上传视频到群相册
**标签**：`群组扩展`

**说明**

上传视频到群相册，封面自动抽取首帧（失败时使用内置默认封面）

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `album_id` | string | 是 | 相册ID |
| `album_name` | string | 是 | 相册名称 |
| `file` | string | 是 | 视频路径、URL或Base64 |

**示例**

```json
{
  "group_id": "123456",
  "album_id": "album_id_1",
  "album_name": "相册1",
  "file": "/path/to/video.mp4"
}
```

<a id="tag-6"></a>

## 6. 用户接口（6）

### `get_cookies`

**摘要**：获取 Cookies
**标签**：`用户接口`

**说明**

获取指定域名的 Cookies

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `domain` | string | 是 | 需要获取 cookies 的域名 |

**示例**

```json
{
  "domain": "qun.qq.com"
}
```

### `get_friend_list`

**摘要**：获取好友列表
**标签**：`用户接口`

**说明**

获取当前帐号的好友列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `no_cache` | boolean / string | 否 | 是否不使用缓存 |

**示例**

官方未提供示例，请按参数表构造。

### `get_recent_contact`

**摘要**：获取最近会话
**标签**：`用户接口`

**说明**

获取最近会话

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `count` | number / string | 是 | 获取的数量（默认 `10`） |

**示例**

```json
{
  "count": 10
}
```

### `send_like`

**摘要**：点赞
**标签**：`用户接口`

**说明**

给指定用户点赞

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 对方 QQ 号 |
| `times` | number / string | 是 | 点赞次数（默认 `1`） |

**示例**

```json
{
  "user_id": "123456",
  "times": 10
}
```

### `set_friend_add_request`

**摘要**：处理加好友请求
**标签**：`用户接口`

**说明**

同意或拒绝加好友请求

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `flag` | string | 是 | 加好友请求的 flag (需从上报中获取) |
| `approve` | string / boolean | 否 | 是否同意请求 |
| `remark` | string | 否 | 添加后的好友备注 |

**示例**

```json
{
  "flag": "flag_12345",
  "approve": true,
  "remark": "新朋友"
}
```

### `set_friend_remark`

**摘要**：设置好友备注
**标签**：`用户接口`

**说明**

设置好友备注

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 对方 QQ 号 |
| `remark` | string | 是 | 备注内容 |

**示例**

```json
{
  "user_id": "123456",
  "remark": "测试备注"
}
```

<a id="tag-7"></a>

## 7. 用户扩展（4）

### `get_friends_with_category`

**摘要**：获取带分组的好友列表
**标签**：`用户扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_profile_like`

**摘要**：获取资料点赞
**标签**：`用户扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 否 | QQ号 |
| `start` | number / string | 是 | 起始位置（默认 `0`） |
| `count` | number / string | 是 | 获取数量（默认 `10`） |

**示例**

```json
{
  "user_id": "123456789",
  "start": 0,
  "count": 10
}
```

### `get_unidirectional_friend_list`

**摘要**：获取单向好友列表
**标签**：`用户扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `set_diy_online_status`

**摘要**：设置自定义在线状态
**标签**：`用户扩展`

**说明**

设置自定义在线状态

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `face_id` | number / string | 是 | 图标ID |
| `face_type` | number / string | 是 | 图标类型（默认 `1`） |
| `wording` | string | 是 | 状态文字内容（默认 ` `） |

**示例**

```json
{
  "face_id": "123",
  "face_type": "1",
  "wording": "自定义状态"
}
```

<a id="tag-8"></a>

## 8. 系统接口（13）

### `can_send_image`

**摘要**：是否可以发送图片
**标签**：`系统接口`

**说明**

检查是否可以发送图片

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `can_send_record`

**摘要**：是否可以发送语音
**标签**：`系统接口`

**说明**

检查是否可以发送语音

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `clean_cache`

**摘要**：清理缓存
**标签**：`系统接口`

**说明**

清理缓存

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_credentials`

**摘要**：获取登录凭证
**标签**：`系统接口`

**说明**

获取登录凭证

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `domain` | string | 是 | 需要获取 cookies 的域名 |

**示例**

```json
{
  "domain": "qun.qq.com"
}
```

### `get_csrf_token`

**摘要**：获取 CSRF Token
**标签**：`系统接口`

**说明**

获取 CSRF Token

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_doubt_friends_add_request`

**摘要**：获取可疑好友申请
**标签**：`系统接口`

**说明**

获取系统的可疑好友申请列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `count` | number | 是 | 获取数量（默认 `50`） |

**示例**

```json
{
  "count": 10
}
```

### `get_group_system_msg`

**摘要**：获取群系统消息
**标签**：`系统接口`

**说明**

获取群系统消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `count` | number / string | 是 | 获取的消息数量（默认 `50`） |

**示例**

```json
{
  "count": 50
}
```

### `get_login_info`

**摘要**：获取登录号信息
**标签**：`系统接口`

**说明**

获取当前登录帐号的信息

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_status`

**摘要**：获取运行状态
**标签**：`系统接口`

**说明**

获取运行状态

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_version_info`

**摘要**：获取版本信息
**标签**：`系统接口`

**说明**

获取版本信息

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `nc_get_packet_status`

**摘要**：获取Packet状态
**标签**：`系统接口`

**说明**

获取底层Packet服务的运行状态

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `set_doubt_friends_add_request`

**摘要**：处理可疑好友申请
**标签**：`系统接口`

**说明**

同意或拒绝系统的可疑好友申请

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `flag` | string | 是 | 请求 flag |
| `approve` | boolean | 是 | 是否同意 (强制为 true)（默认 `True`） |

**示例**

```json
{
  "flag": "12345",
  "approve": true
}
```

### `set_restart`

**摘要**：重启服务
**标签**：`系统接口`

**说明**

重启服务

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

<a id="tag-9"></a>

## 9. 系统扩展（16）

### `add_custom_face`

**摘要**：添加自定义表情
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 是 | 本地表情文件路径 |
| `emoji_id` | string / number | 否 | 表情ID，未提供时传空字符串 |
| `package_id` | string / number | 否 | 表情包ID，未提供时传0 |
| `file_name` | string | 否 | 文件名，未提供时从file路径取basename |
| `file_size` | string / number | 否 | 文件大小，未提供时读取本地文件 |
| `md5` | string | 否 | 文件MD5，未提供时读取本地文件计算 |
| `is_mark_face` | boolean | 否 | 是否商城表情 |
| `is_origin` | boolean | 否 | 是否原图 |

**示例**

```json
{
  "file": "C:\\Users\\Public\\face.png",
  "is_origin": true
}
```

### `bot_exit`

**摘要**：退出登录
**标签**：`系统扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `delete_custom_face`

**摘要**：删除自定义表情
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `res_id` | string / array<string> | 否 |  |
| `id` | string / array<string> | 否 |  |
| `ids` | array<string> | 否 |  |
| `md5` | string / array<string> | 否 |  |

**示例**

```json
{
  "res_id": "2707600964_0_0_0_D8EAA70984B402EE10B0F33DB88F4173_0_0"
}
```

### `fetch_custom_face`

**摘要**：获取自定义表情
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `count` | number / string | 是 | 获取数量（默认 `48`） |

**示例**

```json
{
  "count": 10
}
```

### `fetch_custom_face_detail`

**摘要**：获取自定义表情详情
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `count` | number / string | 是 | 获取数量（默认 `48`） |

**示例**

```json
{
  "count": 10
}
```

### `get_collection_list`

**摘要**：获取收藏列表
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `category` | string | 是 | 分类ID |
| `count` | string | 是 | 获取数量（默认 `50`） |

**示例**

```json
{
  "category": "0",
  "count": "50"
}
```

### `get_mini_app_ark`

**摘要**：获取小程序 Ark
**标签**：`系统扩展`

**参数**

无参数。

**示例**

```json
{
  "type": "bili",
  "title": "测试标题",
  "desc": "测试描述",
  "picUrl": "http://example.com/pic.jpg",
  "jumpUrl": "http://example.com"
}
```

### `get_rkey`

**摘要**：获取扩展 RKey
**标签**：`系统扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_rkey_server`

**摘要**：获取 RKey 服务器
**标签**：`系统扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_robot_uin_range`

**摘要**：获取机器人 UIN 范围
**标签**：`系统扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `nc_get_rkey`

**摘要**：获取 RKey
**标签**：`系统扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `nc_get_user_status`

**摘要**：获取用户在线状态
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | QQ号 |

**示例**

```json
{
  "user_id": "123456789"
}
```

### `send_packet`

**摘要**：发送原始数据包
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `cmd` | string | 是 | 命令字 |
| `data` | string | 是 | 十六进制数据 |
| `rsp` | string / boolean | 是 | 是否等待响应（默认 `True`） |

**示例**

```json
{
  "cmd": "Example.Cmd",
  "data": "123456",
  "rsp": true
}
```

### `set_custom_face_desc`

**摘要**：修改自定义表情描述
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `emoji_id` | number / string | 是 | 表情ID |
| `res_id` | string | 是 | 资源ID |
| `md5` | string | 是 | 表情MD5 |
| `desc` | string | 是 | 新的表情描述 |

**示例**

```json
{
  "emoji_id": 1,
  "res_id": "resource-id",
  "md5": "d41d8cd98f00b204e9800998ecf8427e",
  "desc": "新的描述"
}
```

### `set_input_status`

**摘要**：设置输入状态
**标签**：`系统扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | QQ号 |
| `event_type` | number | 是 | 事件类型 |

**示例**

```json
{
  "user_id": "123456789",
  "event_type": 1
}
```

### `set_online_status`

**摘要**：设置在线状态
**标签**：`系统扩展`

**说明**

## 状态列表

### 在线
```json5;
{ "status": 10, "ext_status": 0, "battery_status": 0; }
```

### Q我吧
```json5;
{ "status": 60, "ext_status": 0, "battery_status": 0; }
```

### 离开
```json5;
{ "status": 30, "ext_status": 0, "battery_status": 0; }
```

### 忙碌
```json5;
{ "status": 50, "ext_status": 0, "battery_status": 0; }
```

### 请勿打扰
```json5;
{ "status": 70, "ext_status": 0, "battery_status": 0; }
```

### 隐身
```json5;
{ "status": 40, "ext_status": 0, "battery_status": 0; }
```

### 听歌中
```json5;
{ "status": 10, "ext_status": 1028, "battery_status": 0; }
```

### 春日限定
```json5;
{ "status": 10, "ext_status": 2037, "battery_status": 0; }
```

### 一起元梦
```json5;
{ "status": 10, "ext_status": 2025, "battery_status": 0; }
```

### 求星搭子
```json5;
{ "status": 10, "ext_status": 2026, "battery_status": 0; }
```

### 被掏空
```json5;
{ "status": 10, "ext_status": 2014, "battery_status": 0; }
```

### 今日天气
```json5;
{ "status": 10, "ext_status": 1030, "battery_status": 0; }
```

### 我crash了
```json5;
{ "status": 10, "ext_status": 2019, "battery_status": 0; }
```

### 爱你
```json5;
{ "status": 10, "ext_status": 2006, "battery_status": 0; }
```

### 恋爱中
```json5;
{ "status": 10, "ext_status": 1051, "battery_status": 0; }
```

### 好运锦鲤
```json5;
{ "status": 10, "ext_status": 1071, "battery_status": 0; }
```

### 水逆退散
```json5;
{ "status": 10, "ext_status": 1201, "battery_status": 0; }
```

### 嗨到飞起
```json5;
{ "status": 10, "ext_status": 1056, "battery_status": 0; }
```

### 元气满满
```json5;
{ "status": 10, "ext_status": 1058, "battery_status": 0; }
```

### 宝宝认证
```json5;
{ "status": 10, "ext_status": 1070, "battery_status": 0; }
```

### 一言难尽
```json5;
{ "status": 10, "ext_status": 1063, "battery_status": 0; }
```

### 难得糊涂
```json5;
{ "status": 10, "ext_status": 2001, "battery_status": 0; }
```

### emo中
```json5;
{ "status": 10, "ext_status": 1401, "battery_status": 0; }
```

### 我太难了
```json5;
{ "status": 10, "ext_status": 1062, "battery_status": 0; }
```

### 我想开了
```json5;
{ "status": 10, "ext_status": 2013, "battery_status": 0; }
```

### 我没事
```json5;
{ "status": 10, "ext_status": 1052, "battery_status": 0; }
```

### 想静静
```json5;
{ "status": 10, "ext_status": 1061, "battery_status": 0; }
```

### 悠哉哉
```json5;
{ "status": 10, "ext_status": 1059, "battery_status": 0; }
```

### 去旅行
```json5;
{ "status": 10, "ext_status": 2015, "battery_status": 0; }
```

### 信号弱
```json5;
{ "status": 10, "ext_status": 1011, "battery_status": 0; }
```

### 出去浪
```json5;
{ "status": 10, "ext_status": 2003, "battery_status": 0; }
```

### 肝作业
```json5;
{ "status": 10, "ext_status": 2012, "battery_status": 0; }
```

### 学习中
```json5;
{ "status": 10, "ext_status": 1018, "battery_status": 0; }
```

### 搬砖中
```json5;
{ "status": 10, "ext_status": 2023, "battery_status": 0; }
```

### 摸鱼中
```json5;
{ "status": 10, "ext_status": 1300, "battery_status": 0; }
```

### 无聊中
```json5;
{ "status": 10, "ext_status": 1060, "battery_status": 0; }
```

### timi中
```json5;
{ "status": 10, "ext_status": 1027, "battery_status": 0; }
```

### 睡觉中
```json5;
{ "status": 10, "ext_status": 1016, "battery_status": 0; }
```

### 熬夜中
```json5;
{ "status": 10, "ext_status": 1032, "battery_status": 0; }
```

### 追剧中
```json5;
{ "status": 10, "ext_status": 1021, "battery_status": 0; }
```

### 我的电量
```json5;
{
  "status": 10,
    "ext_status": 1000,
      "battery_status": 0;
}
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `status` | number / string | 是 | 在线状态 |
| `ext_status` | number / string | 是 | 扩展状态 |
| `battery_status` | number / string | 是 | 电量状态 |

**示例**

```json
{
  "status": 11,
  "ext_status": 0,
  "battery_status": 100
}
```

<a id="tag-10"></a>

## 10. 文件接口（5）

### `get_file`

**摘要**：获取文件
**标签**：`文件接口`

**说明**

获取指定文件的详细信息及下载路径

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 否 | 文件路径、URL或Base64 |
| `file_id` | string | 否 | 文件ID |

**示例**

```json
{
  "file": "file_id_123"
}
```

### `get_group_file_url`

**摘要**：获取群文件URL
**标签**：`文件接口`

**说明**

获取指定群文件的下载链接

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `file_id` | string | 是 | 文件ID |

**示例**

```json
{
  "group_id": "123456",
  "file_id": "file_id_123",
  "busid": 102
}
```

### `get_image`

**摘要**：获取图片
**标签**：`文件接口`

**说明**

获取指定图片的信息及路径

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 否 | 文件路径、URL或Base64 |
| `file_id` | string | 否 | 文件ID |

**示例**

```json
{
  "file": "image_id_123"
}
```

### `get_private_file_url`

**摘要**：获取私聊文件URL
**标签**：`文件接口`

**说明**

获取指定私聊文件的下载链接

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file_id` | string | 是 | 文件ID |

**示例**

```json
{
  "user_id": "123456789",
  "file_id": "file_id_123"
}
```

### `get_record`

**摘要**：获取语音
**标签**：`文件接口`

**说明**

获取指定语音文件的信息，并支持格式转换

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 否 | 文件路径、URL或Base64 |
| `file_id` | string | 否 | 文件ID |
| `out_format` | string | 是 | 输出格式 |

**示例**

```json
{
  "file": "record_id_123",
  "out_format": "mp3"
}
```

<a id="tag-11"></a>

## 11. 文件扩展（17）

### `cancel_online_file`

**摘要**：取消在线文件
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户 QQ |
| `msg_id` | string | 是 | 消息 ID |

**示例**

```json
{
  "user_id": "123456789",
  "msg_id": "123"
}
```

### `create_flash_task`

**摘要**：创建闪传任务
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `files` | array<string> / string | 是 | 文件列表或单个文件路径 |
| `name` | string | 否 | 任务名称 |
| `thumb_path` | string | 否 | 缩略图路径 |
| `validitySeconds` | number | 否 | 文件集有效期（秒），可选 14 天 1209600 / 90 天 7776000 / 180 天 15552000，默认 1209600 |

**示例**

```json
{
  "files": "C:\\test.jpg",
  "name": "test_task",
  "validitySeconds": 1209600
}
```

### `download_fileset`

**摘要**：下载文件集
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fileset_id` | string | 是 | 文件集 ID |

**示例**

```json
{
  "fileset_id": "set_123"
}
```

### `get_fileset_id`

**摘要**：获取文件集 ID
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `share_code` | string | 是 | 分享码或分享链接 |

**示例**

```json
{
  "share_code": "123456"
}
```

### `get_fileset_info`

**摘要**：获取文件集信息
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fileset_id` | string | 是 | 文件集 ID |

**示例**

```json
{
  "fileset_id": "set_123"
}
```

### `get_flash_file_list`

**摘要**：获取闪传文件列表
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fileset_id` | string | 是 | 文件集 ID |

**示例**

```json
{
  "fileset_id": "set_123"
}
```

### `get_flash_file_url`

**摘要**：获取闪传文件链接
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fileset_id` | string | 是 | 文件集 ID |
| `file_name` | string | 否 | 文件名 |
| `file_index` | number | 否 | 文件索引 |

**示例**

```json
{
  "fileset_id": "set_123"
}
```

### `get_online_file_msg`

**摘要**：获取在线文件消息
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户 QQ |

**示例**

```json
{
  "user_id": "123456789"
}
```

### `get_share_link`

**摘要**：获取文件分享链接
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fileset_id` | string | 是 | 文件集 ID |

**示例**

```json
{
  "fileset_id": "set_123"
}
```

### `move_group_file`

**摘要**：移动群文件
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `file_id` | string | 是 | 文件ID |
| `current_parent_directory` | string | 是 | 当前父目录 |
| `target_parent_directory` | string | 是 | 目标父目录 |

**示例**

```json
{
  "group_id": "123456",
  "file_id": "/file_id",
  "current_parent_directory": "/current_folder_id",
  "target_parent_directory": "/target_folder_id"
}
```

### `receive_online_file`

**摘要**：接收在线文件
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户 QQ |
| `msg_id` | string | 是 | 消息 ID |
| `element_id` | string | 是 | 元素 ID |

**示例**

```json
{
  "user_id": "123456789",
  "msg_id": "123",
  "save_path": "C:\\save"
}
```

### `refuse_online_file`

**摘要**：拒绝在线文件
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户 QQ |
| `msg_id` | string | 是 | 消息 ID |
| `element_id` | string | 是 | 元素 ID |

**示例**

```json
{
  "user_id": "123456789",
  "msg_id": "123"
}
```

### `rename_group_file`

**摘要**：重命名群文件
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `file_id` | string | 是 | 文件ID |
| `current_parent_directory` | string | 是 | 当前父目录 |
| `new_name` | string | 是 | 新文件名 |

**示例**

```json
{
  "group_id": "123456",
  "file_id": "/file_id",
  "current_parent_directory": "/",
  "new_name": "new_name.jpg"
}
```

### `send_flash_msg`

**摘要**：发送闪传消息
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fileset_id` | string | 是 | 文件集 ID |
| `user_id` | string | 否 | 用户 QQ |
| `group_id` | string | 否 | 群号 |

**示例**

```json
{
  "fileset_id": "set_123",
  "user_id": "123456789"
}
```

### `send_online_file`

**摘要**：发送在线文件
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户 QQ |
| `file_path` | string | 是 | 本地文件路径 |
| `file_name` | string | 否 | 文件名 (可选) |

**示例**

```json
{
  "user_id": "123456789",
  "file_path": "C:\\path\\to\\file.txt",
  "file_name": "test.txt"
}
```

### `send_online_folder`

**摘要**：发送在线文件夹
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户 QQ |
| `folder_path` | string | 是 | 本地文件夹路径 |
| `folder_name` | string | 否 | 文件夹名称 (可选) |

**示例**

```json
{
  "user_id": "123456789",
  "folder_path": "C:\\path\\to\\folder"
}
```

### `trans_group_file`

**摘要**：传输群文件
**标签**：`文件扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `file_id` | string | 是 | 文件ID |

**示例**

```json
{
  "group_id": "123456",
  "file_id": "/file_id"
}
```

<a id="tag-12"></a>

## 12. 流式接口（2）

### `download_file_stream`

**摘要**：下载文件流
**标签**：`流式接口`

**说明**

以流式方式从网络或本地下载文件

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 否 | 文件路径或 URL |
| `file_id` | string | 否 | 文件 ID |
| `chunk_size` | number | 否 | 分块大小 (字节)（默认 `65536`） |

**示例**

```json
{
  "file": "http://example.com/file.png"
}
```

### `upload_file_stream`

**摘要**：上传文件流
**标签**：`流式接口`

**说明**

以流式方式上传文件数据到机器人

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `stream_id` | string | 是 | 流 ID |
| `chunk_data` | string | 否 | 分块数据 (Base64) |
| `chunk_index` | number | 否 | 分块索引 |
| `total_chunks` | number | 否 | 总分块数 |
| `file_size` | number | 否 | 文件总大小 |
| `expected_sha256` | string | 否 | 期望的 SHA256 |
| `is_complete` | boolean | 否 | 是否完成 |
| `filename` | string | 否 | 文件名 |
| `reset` | boolean | 否 | 是否重置 |
| `verify_only` | boolean | 否 | 是否仅验证 |
| `file_retention` | number | 是 | 文件保留时间 (毫秒)（默认 `300000`） |

**示例**

```json
{
  "stream_id": "uuid-1234-5678",
  "chunk_data": "SGVsbG8gV29ybGQ=",
  "chunk_index": 0,
  "total_chunks": 1,
  "file_size": 11
}
```

<a id="tag-13"></a>

## 13. 流式传输扩展（4）

### `clean_stream_temp_file`

**摘要**：清理流式传输临时文件
**标签**：`流式传输扩展`

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `download_file_image_stream`

**摘要**：下载图片文件流
**标签**：`流式传输扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 否 | 文件路径或 URL |
| `file_id` | string | 否 | 文件 ID |
| `chunk_size` | number | 否 | 分块大小 (字节)（默认 `65536`） |

**示例**

```json
{
  "file": "image_file_id"
}
```

### `download_file_record_stream`

**摘要**：下载语音文件流
**标签**：`流式传输扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 否 | 文件路径或 URL |
| `file_id` | string | 否 | 文件 ID |
| `chunk_size` | number | 否 | 分块大小 (字节)（默认 `65536`） |
| `out_format` | string | 否 | 输出格式 |

**示例**

```json
{
  "file": "record_file_id"
}
```

### `test_download_stream`

**摘要**：测试下载流
**标签**：`流式传输扩展`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `error` | boolean | 否 | 是否触发测试错误（默认 `False`） |

**示例**

```json
{
  "url": "http://example.com/file"
}
```

<a id="tag-14"></a>

## 14. 频道接口（2）

### `get_guild_list`

**摘要**：获取频道列表
**标签**：`频道接口`

**说明**

获取当前帐号已加入的频道列表

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_guild_service_profile`

**摘要**：获取频道个人信息
**标签**：`频道接口`

**说明**

获取当前帐号在频道中的个人资料

**参数**

无参数。

**示例**

```json
{
  "guild_id": "123456"
}
```

<a id="tag-15"></a>

## 15. 扩展接口（24）

### `.ocr_image`

**摘要**：图片 OCR 识别 (内部)
**标签**：`扩展接口`

**说明**

识别图片中的文字内容(仅Windows端支持)

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `image` | string | 是 | 图片路径、URL或Base64 |

**示例**

```json
{
  "image": "image_id_123"
}
```

### `comment_qzone`

**摘要**：评论QQ空间说说
**标签**：`扩展接口`

**说明**

传 tid 使用 SnowLuma 参数，一级评论支持 images；回复须成对提供 comment_id/comment_uin，指定接收者时还需 reply_uin/reply_name，楼中楼仅文字。传 feed_ref 则保留原 comment/reply_user 方式及原始结果；两种参数不能混用。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed_ref` | object | 否 | 原样传回列表或详情返回的 feed_ref；整体不得超过 64 KiB |
| `tid` | string / integer | 否 |  |
| `target_uin` | string / integer | 否 |  |
| `content` | string / number / boolean | 是 |  |
| `comment` | object | 否 | 从详情 comments 中取得的完整父评论对象 |
| `reply_user` | object | 否 |  |
| `comment_id` | string / integer | 否 |  |
| `comment_uin` | string / integer | 否 |  |
| `reply_uin` | string / integer | 否 |  |
| `reply_name` | string / number / boolean | 否 |  |
| `images` | array<string> | 否 | 图片来源数组，支持 file://、HTTP(S)、base64://；仅一级评论支持图片 |

**示例**

```json
{
  "tid": "sample-post",
  "target_uin": "10002",
  "content": "很有意思"
}
```

### `create_collection`

**摘要**：创建收藏
**标签**：`扩展接口`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `rawData` | string | 是 | 原始数据 |
| `brief` | string | 是 | 简要描述 |

**示例**

```json
{
  "rawData": "收藏内容",
  "brief": "收藏标题"
}
```

### `delete_qzone_msg`

**摘要**：删除QQ空间说说
**标签**：`扩展接口`

**说明**

删除QQ空间(Qzone)的一条说说, 按 tid 删除

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `tid` | string / integer | 是 |  |

**示例**

```json
{
  "tid": "1234567890abcdef1234567890"
}
```

### `get_ai_characters`

**摘要**：获取AI角色列表
**标签**：`扩展接口`

**说明**

获取群聊中的AI角色列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `chat_type` | number / string | 是 | 聊天类型（默认 `1`） |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_clientkey`

**摘要**：获取ClientKey
**标签**：`扩展接口`

**说明**

获取当前登录帐号的ClientKey

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_qzone_comment_list`

**摘要**：获取QQ空间说说评论
**标签**：`扩展接口`

**说明**

不传 cursor 读取详情中的首批评论，之后用返回的 feed_ref 和 next_cursor 续页。返回作者、正文、图片、赞数、内联回复及完整原始对象；未知值为 null，不自动拉取全部历史。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed_ref` | object | 是 | 原样传回列表或详情返回的 feed_ref；整体不得超过 64 KiB |
| `cursor` | string | 否 | 上一页返回的 next_cursor；不传时读取第一页，游标不能跨账号或查询使用 |

**示例**

```json
{
  "feed_ref": {
    "union_id": {
      "uf_key": "feed-key",
      "ugc_id": "shuoshuo-tid",
      "feed_id": "feed-id"
    },
    "feed_action_domain_type": 1,
    "like_key": "like-key"
  }
}
```

### `get_qzone_comment_replies`

**摘要**：获取QQ空间评论楼中楼回复
**标签**：`扩展接口`

**说明**

传入读取结果的完整 comment，使用其回复游标读取追加回复；之后用返回的 feed_ref、同一父评论和 next_cursor 续页。与内联回复按 ID 合并，不自动拉取全部历史；每页使用空间固定页大小。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed_ref` | object | 是 | 原样传回列表或详情返回的 feed_ref；整体不得超过 64 KiB |
| `comment` | object | 是 | 原样传回读取结果中的完整 comment 对象；整体不得超过64KiB |
| `cursor` | string | 否 | 上一页返回的 next_cursor；不传时读取第一页，游标不能跨账号或查询使用 |

**示例**

```json
{
  "feed_ref": {
    "union_id": {
      "uf_key": "feed-key",
      "ugc_id": "shuoshuo-tid",
      "feed_id": "feed-id"
    },
    "feed_action_domain_type": 1,
    "like_key": "like-key"
  },
  "comment": {
    "id": 0,
    "user": {
      "uid": "u_commenter",
      "uin": "",
      "nick": "评论作者",
      "portrait": "https://example.com/avatar.png"
    },
    "time": 1792926000,
    "content": [
      {
        "type": 0,
        "content": "很有意思"
      }
    ],
    "media_items": [],
    "like": {
      "id": "comment-like-key",
      "count": 2,
      "status": 1
    },
    "reply_num": 1,
    "has_more_reply": true,
    "replys": [],
    "reply_attach_info": "server-reply-pointer"
  }
}
```

### `get_qzone_feeds`

**摘要**：获取QQ空间好友动态
**标签**：`扩展接口`

**说明**

默认返回 SnowLuma 格式，page_num 默认1、count 默认10，续页原样传 cursor。format=native 返回原 H5 Feed 和 feed_ref；旧 native 游标可自动识别，native 模式不接受 page_num/count。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `format` | string | 否 | 默认 snowluma；native 保留原来的 H5 列表格式（可选：`snowluma`, `native`） |
| `page_num` | integer / string | 否 |  |
| `count` | integer / string | 否 |  |
| `cursor` | string | 否 |  |

**示例**

```json
{
  "page_num": 1,
  "count": 10
}
```

### `get_qzone_msg_detail`

**摘要**：获取QQ空间说说详情
**标签**：`扩展接口`

**说明**

传 tid 返回 SnowLuma 详情和评论，target_uin 默认当前账号、pos 默认0、num 默认20。传完整 feed_ref 则保留原 H5 详情、原始评论和续页信息；两种定位方式不能混用。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed_ref` | object | 否 | 原样传回列表或详情返回的 feed_ref；整体不得超过 64 KiB |
| `tid` | string / integer | 否 |  |
| `target_uin` | string / integer | 否 |  |
| `pos` | integer / string | 否 |  |
| `num` | integer / string | 否 |  |

**示例**

```json
{
  "tid": "sample-post",
  "pos": 0,
  "num": 20
}
```

### `get_qzone_msg_list`

**摘要**：获取QQ空间说说列表
**标签**：`扩展接口`

**说明**

默认返回 SnowLuma 的 total/msglist，pos 默认0、num 默认20（1至100）。format=native 保留原 H5 Feed、feed_ref 和游标；仅传旧 cursor 也会选择 native。两种分页参数不能混用。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `format` | string | 否 | 默认 snowluma；native 保留原来的 H5 列表格式（可选：`snowluma`, `native`） |
| `target_uin` | string / integer | 否 |  |
| `pos` | integer / string | 否 |  |
| `num` | integer / string | 否 |  |
| `cursor` | string | 否 | 上一页返回的 next_cursor；不传时读取第一页，游标不能跨账号或查询使用 |

**示例**

```json
{
  "target_uin": "10001",
  "pos": 0,
  "num": 20
}
```

### `get_qzone_profile`

**摘要**：获取QQ空间资料
**标签**：`扩展接口`

**说明**

获取空间名称和空间说明；target_uin 不传时读取当前账号，空名称或说明按原值返回。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `target_uin` | string / integer | 否 | 空间所属 QQ 号；不传时为当前账号 |

**示例**

```json
{
  "target_uin": "10001"
}
```

### `like_qzone`

**摘要**：点赞QQ空间说说
**标签**：`扩展接口`

**说明**

支持 SnowLuma 的 tid、target_uin 和 abstime（默认0）；传 feed_ref 则沿用原 H5 点赞方式。两种定位方式不能混用，写入失败不会切换接口重试。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed_ref` | object | 否 | 原样传回列表或详情返回的 feed_ref；整体不得超过 64 KiB |
| `tid` | string / integer | 否 |  |
| `target_uin` | string / integer | 否 |  |
| `abstime` | integer / string | 否 |  |

**示例**

```json
{
  "tid": "sample-post",
  "target_uin": "10002",
  "abstime": 1700000000
}
```

### `ocr_image`

**摘要**：图片 OCR 识别
**标签**：`扩展接口`

**说明**

识别图片中的文字内容(仅Windows端支持)

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `image` | string | 是 | 图片路径、URL或Base64 |

**示例**

```json
{
  "image": "image_id_123"
}
```

### `send_qzone_msg`

**摘要**：发表QQ空间说说
**标签**：`扩展接口`

**说明**

在QQ空间(Qzone)发表说说, 支持纯文字或带(多)图, 可设置查看权限。纯文字使用QQ内置空间接口, 图片保留原有上传和发表方式

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content` | string / number / boolean | 是 |  |
| `images` | array<string> | 否 | 图片数组, 支持 file:// http(s):// base64:// , 自动上传 |
| `ugc_right` | number / string | 否 | 查看权限: 1所有人可见 4好友可见 16部分好友可见 64仅自己可见 128部分好友不可见（默认 `1`） |
| `target_uins` | array<number / string> | 否 | ugc_right为16/128时, 权限作用的QQ号数组 |

**示例**

```json
{
  "content": "今天天气不错",
  "images": [],
  "ugc_right": 1,
  "target_uins": []
}
```

### `set_group_kick_members`

**摘要**：批量踢出群成员
**标签**：`扩展接口`

**说明**

从指定群聊中批量踢出多个成员

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `user_id` | array<string> | 是 | QQ号列表 |
| `reject_add_request` | boolean / string | 否 | 是否拒绝加群请求 |

**示例**

```json
{
  "group_id": "123456",
  "user_id": [
    "123456789"
  ],
  "reject_add_request": false
}
```

### `set_group_special_title`

**摘要**：设置专属头衔
**标签**：`扩展接口`

**说明**

设置群聊中指定成员的专属头衔

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `user_id` | string | 是 | QQ号 |
| `special_title` | string | 是 | 专属头衔（默认 ``） |

**示例**

```json
{
  "group_id": "123456",
  "user_id": "123456789",
  "special_title": "头衔"
}
```

### `set_qq_avatar`

**摘要**：设置QQ头像
**标签**：`扩展接口`

**说明**

修改当前账号的QQ头像

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 是 | 图片路径、URL或Base64 |

**示例**

```json
{
  "file": "base64://..."
}
```

### `set_qzone_ban`

**摘要**：设置QQ空间访问限制
**标签**：`扩展接口`

**说明**

在当前账号的空间设置指定用户的访问限制；enable 默认为 true，传 false 取消禁止。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string / integer | 是 | 需要设置空间访问限制的QQ号 |
| `enable` | boolean / integer / string | 否 | 默认true；支持布尔值及true/false、1/0、yes/no、on/off拼写 |

**示例**

```json
{
  "user_id": "10002",
  "enable": true
}
```

### `set_qzone_msg_right`

**摘要**：修改QQ空间说说权限
**标签**：`扩展接口`

**说明**

仅修改当前账号发表的说说。ugc_right 为16或128时 target_uins 不能为空；其他权限不使用该列表。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `tid` | string / integer | 是 |  |
| `ugc_right` | number / string | 是 | 查看权限：1所有人，4好友，16部分好友，64仅自己，128排除部分好友 |
| `target_uins` | array<string / integer> | 否 | ugc_right 为16或128时的QQ号列表 |

**示例**

```json
{
  "tid": "shuoshuo-tid",
  "ugc_right": 4
}
```

### `set_qzone_profile`

**摘要**：修改QQ空间资料
**标签**：`扩展接口`

**说明**

仅修改当前账号的空间名称或说明，至少提供一项。省略字段保持不变；空字符串清空字段；数字和布尔值转换为字符串。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | string / number / boolean | 否 | 空间名称；空字符串表示清空，省略时不修改 |
| `description` | string / number / boolean | 否 | 空间说明；空字符串表示清空，省略时不修改 |

**示例**

```json
{
  "name": "我的空间",
  "description": "记录生活"
}
```

### `set_self_longnick`

**摘要**：设置个性签名
**标签**：`扩展接口`

**说明**

修改当前登录帐号的个性签名

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `longNick` | string | 是 | 签名内容 |

**示例**

```json
{
  "longNick": "个性签名"
}
```

### `translate_en2zh`

**摘要**：英文单词翻译
**标签**：`扩展接口`

**说明**

将英文单词列表翻译为中文

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `words` | array<string> | 是 | 待翻译单词列表 |

**示例**

```json
{
  "words": [
    "hello"
  ]
}
```

### `unlike_qzone`

**摘要**：取消QQ空间说说点赞
**标签**：`扩展接口`

**说明**

支持 SnowLuma 的 tid、target_uin 和 abstime（默认0）；传 feed_ref 则沿用原 H5 取消点赞方式。两种定位方式不能混用，写入失败不会切换接口重试。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed_ref` | object | 否 | 原样传回列表或详情返回的 feed_ref；整体不得超过 64 KiB |
| `tid` | string / integer | 否 |  |
| `target_uin` | string / integer | 否 |  |
| `abstime` | integer / string | 否 |  |

**示例**

```json
{
  "tid": "sample-post",
  "target_uin": "10002",
  "abstime": 1700000000
}
```

<a id="tag-16"></a>

## 16. QQ空间扩展（14）

### `comment_qzone_public_feed`

**摘要**：评论空友爱看动态
**标签**：`QQ空间扩展`

**说明**

对完整 feed 发表评论；content 接受非空文本或富文本对象数组，富文本字段原样保留

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `content` | string / array<object> | 是 | 非空文本或非空富文本对象数组，保留每个对象的全部字段 |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "content": "很有意思"
}
```

### `delete_qzone_public_comment`

**摘要**：删除空友爱看评论
**标签**：`QQ空间扩展`

**说明**

传入完整 feed 及 comment 删除评论，操作权限由上游校验

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `comment` | object | 是 | 详情或评论列表返回的完整 comment 对象，请保留 like.id 等全部字段 |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "comment": {
    "id": "example-comment",
    "like": {
      "id": "example-comment-like"
    },
    "reply_attach_info": ""
  }
}
```

### `delete_qzone_public_reply`

**摘要**：删除空友爱看回复
**标签**：`QQ空间扩展`

**说明**

传入完整 feed、父 comment 和目标 reply 删除回复，操作权限由上游校验

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `comment` | object | 是 | 详情或评论列表返回的完整 comment 对象，请保留 like.id 等全部字段 |
| `reply` | object | 是 | 回复列表返回的完整 reply 对象，请保留全部字段 |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "comment": {
    "id": "example-comment",
    "like": {
      "id": "example-comment-like"
    },
    "reply_attach_info": ""
  },
  "reply": {
    "id": "example-reply",
    "like": {
      "id": "example-reply-like"
    }
  }
}
```

### `forward_qzone_public_feed`

**摘要**：转发空友爱看动态
**标签**：`QQ空间扩展`

**说明**

将完整 feed 转发到自己的空间，可通过 reason 添加转发附言

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `reason` | string | 否 | 转发附言，默认空字符串；数字或布尔值会转为文本（默认 ``） |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "reason": "分享一条动态"
}
```

### `get_qzone_public_capabilities`

**摘要**：获取空友爱看接口能力
**标签**：`QQ空间扩展`

**说明**

获取当前 QQ 版本和账号可用的空友爱看接口能力，不会执行写操作

**参数**

无参数。

**示例**

官方未提供示例。无参数 action 可直接调用 `{}`。

### `get_qzone_public_comments`

**摘要**：获取空友爱看评论
**标签**：`QQ空间扩展`

**说明**

读取动态的后续评论；cursor 为必填非空字符串，使用动态详情或上一评论页的 attach_info，原始评论对象应完整保留

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `cursor` | string | 是 | 动态详情或上一评论页返回的非空 attach_info；数字或布尔值会转为文本 |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "cursor": "detail-attach-info"
}
```

### `get_qzone_public_feed_detail`

**摘要**：获取空友爱看动态详情
**标签**：`QQ空间扩展`

**说明**

传入列表中的完整 feed 对象获取详情；继续读取评论时，将详情返回的 attach_info 作为 cursor

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  }
}
```

### `get_qzone_public_feeds`

**摘要**：获取空友爱看动态
**标签**：`QQ空间扩展`

**说明**

获取空友爱看动态列表；后续操作应直接传入 feeds 中的完整对象，翻页使用 next_cursor

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `cursor` | string | 否 | 上一页返回的非空 next_cursor，首次请求可省略；数字或布尔值会转为文本 |

**示例**

官方未提供示例，请按参数表构造。

### `get_qzone_public_replies`

**摘要**：获取空友爱看评论回复
**标签**：`QQ空间扩展`

**说明**

传入完整动态及父评论读取回复分页；省略 cursor 时使用父评论中的 reply_attach_info

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `comment` | object | 是 | 详情或评论列表返回的完整 comment 对象，请保留 like.id 等全部字段 |
| `cursor` | string | 否 | 回复分页游标，默认为空字符串；空字符串时使用 comment.reply_attach_info；数字或布尔值会转为文本（默认 ``） |
| `page_size` | number / string | 否 | 每页回复数量，默认 20；有限数字或非空数值字符串，向零截断后应大于等于 1（默认 `20`） |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "comment": {
    "id": "example-comment",
    "like": {
      "id": "example-comment-like"
    },
    "reply_attach_info": ""
  },
  "page_size": 20
}
```

### `reply_qzone_public_feed`

**摘要**：回复空友爱看评论
**标签**：`QQ空间扩展`

**说明**

传入完整 feed、父 comment 及非空 content 发表回复；需要回复已有回复时一并传入完整 reply

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `comment` | object | 是 | 详情或评论列表返回的完整 comment 对象，请保留 like.id 等全部字段 |
| `content` | string / array<object> | 是 | 非空文本或非空富文本对象数组，保留每个对象的全部字段 |
| `reply` | object | 否 | 回复列表返回的完整 reply 对象，请保留全部字段 |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "comment": {
    "id": "example-comment",
    "like": {
      "id": "example-comment-like"
    },
    "reply_attach_info": ""
  },
  "content": "谢谢分享"
}
```

### `set_qzone_public_comment_like`

**摘要**：设置空友爱看评论或回复赞
**标签**：`QQ空间扩展`

**说明**

对完整 comment 点赞或取消点赞；传入完整 reply 时操作该回复，保留 comment/reply 的 like.id 等字段

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `comment` | object | 是 | 详情或评论列表返回的完整 comment 对象，请保留 like.id 等全部字段 |
| `reply` | object | 否 | 回复列表返回的完整 reply 对象，请保留全部字段 |
| `enable` | boolean / number / string | 否 | 是否启用，默认 true；数字非 0 为 true，文本支持 true/false、1/0、yes/no、on/off（默认 `True`） |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "comment": {
    "id": "example-comment",
    "like": {
      "id": "example-comment-like"
    },
    "reply_attach_info": ""
  },
  "enable": true
}
```

### `set_qzone_public_follow`

**摘要**：蹲或取消蹲空友爱看作者
**标签**：`QQ空间扩展`

**说明**

根据完整 feed 蹲或取消蹲动态作者；enable 默认 true，返回上游操作结果

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `enable` | boolean / number / string | 否 | 是否启用，默认 true；数字非 0 为 true，文本支持 true/false、1/0、yes/no、on/off（默认 `True`） |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "enable": true
}
```

### `set_qzone_public_like`

**摘要**：设置空友爱看普通赞
**标签**：`QQ空间扩展`

**说明**

对完整 feed 设置或取消普通点赞（like）；enable 默认 true，此操作与推分别处理

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `enable` | boolean / number / string | 否 | 是否启用，默认 true；数字非 0 为 true，文本支持 true/false、1/0、yes/no、on/off（默认 `True`） |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "enable": true
}
```

### `set_qzone_public_upvote`

**摘要**：推或取消推空友爱看动态
**标签**：`QQ空间扩展`

**说明**

对完整 feed 设置推或取消推（upvote）；enable 默认 true，此操作与普通点赞分别处理

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | object | 是 | get_qzone_public_feeds 返回的完整 feed 对象，请保留全部字段 |
| `enable` | boolean / number / string | 否 | 是否启用，默认 true；数字非 0 为 true，文本支持 true/false、1/0、yes/no、on/off（默认 `True`） |

**示例**

```json
{
  "feed": {
    "cell_common": {
      "union_id": {
        "uf_key": "example-uf-key",
        "ugc_id": "example-ugc-id",
        "feed_id": "example-feed-id",
        "ext_ids": []
      },
      "cur_like_key": "example-like-key",
      "domain_type": 3
    },
    "cell_user_info": {
      "user": {
        "uin": "10001"
      }
    },
    "cell_feed_transfer": {}
  },
  "enable": true
}
```

<a id="tag-17"></a>

## 17. AI 扩展（2）

### `get_ai_record`

**摘要**：获取 AI 语音
**标签**：`AI 扩展`

**说明**

通过 AI 语音引擎获取指定文本的语音 URL

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `character` | string | 是 | 角色ID |
| `group_id` | string | 是 | 群号 |
| `text` | string | 是 | 语音文本内容 |

**示例**

```json
{
  "character": "ai_char_1",
  "group_id": "123456",
  "text": "你好"
}
```

### `send_group_ai_record`

**摘要**：发送群 AI 语音
**标签**：`AI 扩展`

**说明**

发送 AI 生成的语音到指定群聊

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `character` | string | 是 | 角色ID |
| `group_id` | string | 是 | 群号 |
| `text` | string | 是 | 语音文本内容 |

**示例**

```json
{
  "character": "ai_char_1",
  "group_id": "123456",
  "text": "你好"
}
```

<a id="tag-18"></a>

## 18. Go-CQHTTP（27）

### `.handle_quick_operation`

**摘要**：处理快速操作
**标签**：`Go-CQHTTP`

**说明**

处理来自事件上报的快速操作请求

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `context` | object | 是 | 事件上下文 |
| `operation` | object | 是 | 快速操作内容 |

**示例**

```json
{
  "context": {},
  "operation": {}
}
```

### `_get_model_show`

**摘要**：获取机型显示
**标签**：`Go-CQHTTP`

**说明**

获取当前账号可用的设备机型显示名称列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 否 | 模型名称 |

**示例**

```json
{
  "model": "iPhone 13"
}
```

### `_send_group_notice`

**摘要**：发送群公告
**标签**：`Go-CQHTTP`

**说明**

在指定群聊中发布新的公告

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `content` | string | 是 | 公告内容 |
| `image` | string | 否 | 公告图片路径或 URL |
| `pinned` | number / string | 是 | 是否置顶 (0/1)（默认 `0`） |
| `type` | number / string | 是 | 类型 (默认为 1)（默认 `1`） |
| `confirm_required` | number / string | 是 | 是否需要确认 (0/1)（默认 `1`） |
| `is_show_edit_card` | number / string | 是 | 是否显示修改群名片引导 (0/1)（默认 `0`） |
| `tip_window_type` | number / string | 是 | 弹窗类型 (默认为 0)（默认 `0`） |

**示例**

```json
{
  "group_id": "123456",
  "content": "公告内容",
  "image": "base64://..."
}
```

### `_set_model_show`

**摘要**：设置机型
**标签**：`Go-CQHTTP`

**说明**

设置当前账号的设备机型名称

**参数**

无参数。

**示例**

```json
{
  "model": "iPhone 13",
  "model_show": "iPhone 13"
}
```

### `check_url_safely`

**摘要**：检查URL安全性
**标签**：`Go-CQHTTP`

**说明**

检查指定URL的安全等级

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `url` | string | 是 | 要检查的 URL |

**示例**

```json
{
  "url": "https://example.com"
}
```

### `create_group_file_folder`

**摘要**：创建群文件目录
**标签**：`Go-CQHTTP`

**说明**

在群文件系统中创建新的文件夹

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `folder_name` | string | 否 | 文件夹名称 |
| `name` | string | 否 | 文件夹名称 |

**示例**

```json
{
  "group_id": "123456789",
  "folder_name": "新建文件夹"
}
```

### `delete_friend`

**摘要**：删除好友
**标签**：`Go-CQHTTP`

**说明**

从好友列表中删除指定用户

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `friend_id` | string / number | 否 | 好友 QQ 号 |
| `user_id` | string / number | 否 | 用户 QQ 号 |
| `temp_block` | boolean | 否 | 是否加入黑名单 |
| `temp_both_del` | boolean | 否 | 是否双向删除 |

**示例**

```json
{
  "user_id": "123456789"
}
```

### `delete_group_file`

**摘要**：删除群文件
**标签**：`Go-CQHTTP`

**说明**

在群文件系统中删除指定的文件

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `file_id` | string | 是 | 文件ID |
| `bus_id` | number | 否 | 文件业务ID，默认使用文件列表中的 busid |
| `busid` | number | 否 | 文件业务ID，兼容 busid 字段 |

**示例**

```json
{
  "group_id": "123456",
  "file_id": "file_uuid_123",
  "bus_id": 104
}
```

### `delete_group_folder`

**摘要**：删除群文件目录
**标签**：`Go-CQHTTP`

**说明**

在群文件系统中删除指定的文件夹

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `folder_id` | string | 否 | 文件夹ID |
| `folder` | string | 否 | 文件夹ID |

**示例**

```json
{
  "group_id": "123456",
  "folder_id": "folder_uuid_123"
}
```

### `download_file`

**摘要**：下载文件
**标签**：`Go-CQHTTP`

**说明**

下载网络文件到本地临时目录

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `url` | string | 否 | 下载链接 |
| `base64` | string | 否 | base64数据 |
| `name` | string | 否 | 文件名 |
| `headers` | string / array<string> | 否 | 请求头 |

**示例**

```json
{
  "url": "https://example.com/file.png",
  "thread_count": 1,
  "headers": "User-Agent: NapCat"
}
```

### `get_forward_msg`

**摘要**：获取合并转发消息
**标签**：`Go-CQHTTP`

**说明**

获取合并转发消息的具体内容

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_id` | string | 否 | 消息ID |
| `id` | string | 否 | 消息ID |

**示例**

```json
{
  "message_id": "123456"
}
```

### `get_friend_msg_history`

**摘要**：获取好友历史消息
**标签**：`Go-CQHTTP`

**说明**

获取指定好友的历史聊天记录

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户QQ |
| `message_seq` | string | 否 | 起始消息序号 |
| `count` | number | 是 | 获取消息数量（默认 `20`） |
| `reverse_order` | boolean | 是 | 是否反向排序（默认 `False`） |
| `disable_get_url` | boolean | 是 | 是否禁用获取URL（默认 `False`） |
| `parse_mult_msg` | boolean | 是 | 是否解析合并消息（默认 `True`） |
| `quick_reply` | boolean | 是 | 是否快速回复（默认 `False`） |
| `reverseOrder` | boolean | 是 | 是否反向排序(旧版本兼容)（默认 `False`） |

**示例**

```json
{
  "user_id": "123456789",
  "message_seq": 0,
  "count": 20
}
```

### `get_group_at_all_remain`

**摘要**：获取群艾特全体剩余次数
**标签**：`Go-CQHTTP`

**说明**

获取指定群聊中艾特全体成员的剩余次数

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_group_file_system_info`

**摘要**：获取群文件系统信息
**标签**：`Go-CQHTTP`

**说明**

获取群聊文件系统的空间及状态信息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_group_files_by_folder`

**摘要**：获取群文件夹文件列表
**标签**：`Go-CQHTTP`

**说明**

获取指定群文件夹下的文件及子文件夹列表

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `folder_id` | string | 否 | 文件夹ID |
| `folder` | string | 否 | 文件夹ID |
| `file_count` | number / string | 是 | 文件数量（默认 `50`） |

**示例**

```json
{
  "group_id": "123456",
  "folder_id": "folder_id"
}
```

### `get_group_honor_info`

**摘要**：获取群荣誉信息
**标签**：`Go-CQHTTP`

**说明**

获取指定群聊的荣誉信息，如龙王等

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `type` | string | 否 | 荣誉类型（可选：`all`, `talkative`, `performer`, `legend`, `strong_newbie`, `emotion`） |

**示例**

```json
{
  "group_id": "123456",
  "type": "all"
}
```

### `get_group_msg_history`

**摘要**：获取群历史消息
**标签**：`Go-CQHTTP`

**说明**

获取指定群聊的历史聊天记录

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `message_seq` | string | 否 | 起始消息序号 |
| `count` | number | 是 | 获取消息数量（默认 `20`） |
| `reverse_order` | boolean | 是 | 是否反向排序（默认 `False`） |
| `disable_get_url` | boolean | 是 | 是否禁用获取URL（默认 `False`） |
| `parse_mult_msg` | boolean | 是 | 是否解析合并消息（默认 `True`） |
| `quick_reply` | boolean | 是 | 是否快速回复（默认 `False`） |
| `reverseOrder` | boolean | 是 | 是否反向排序(旧版本兼容)（默认 `False`） |

**示例**

```json
{
  "group_id": "123456",
  "message_seq": 0,
  "count": 20
}
```

### `get_group_root_files`

**摘要**：获取群根目录文件列表
**标签**：`Go-CQHTTP`

**说明**

获取群文件根目录下的所有文件和文件夹

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `file_count` | number / string | 是 | 文件数量（默认 `50`） |

**示例**

```json
{
  "group_id": "123456"
}
```

### `get_online_clients`

**摘要**：获取在线客户端
**标签**：`Go-CQHTTP`

**说明**

获取当前登录账号的在线客户端列表

**参数**

无参数。

**示例**

```json
{
  "no_cache": false
}
```

### `get_stranger_info`

**摘要**：获取陌生人信息
**标签**：`Go-CQHTTP`

**说明**

获取指定非好友用户的信息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户QQ |
| `no_cache` | boolean / string | 是 | 是否不使用缓存（默认 `False`） |

**示例**

```json
{
  "user_id": "123456789"
}
```

### `send_forward_msg`

**摘要**：发送合并转发消息
**标签**：`Go-CQHTTP`

**说明**

发送合并转发消息

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_type` | string | 否 | 消息类型 (private/group)（可选：`private`, `group`） |
| `user_id` | string | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message` | OB11MessageMixType | 是 |  |
| `auto_escape` | boolean / string | 否 | 是否作为纯文本发送 |
| `source` | string | 否 | 合并转发来源 |
| `news` | array<object> | 否 | 合并转发新闻 |
| `summary` | string | 否 | 合并转发摘要 |
| `prompt` | string | 否 | 合并转发提示 |
| `timeout` | number | 否 | 自定义发送超时(毫秒)，覆盖自动计算值 |

**示例**

```json
{
  "group_id": "123456789",
  "messages": []
}
```

### `send_group_forward_msg`

**摘要**：发送群合并转发消息
**标签**：`Go-CQHTTP`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_type` | string | 否 | 消息类型 (private/group)（可选：`private`, `group`） |
| `user_id` | string | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message` | OB11MessageMixType | 是 |  |
| `auto_escape` | boolean / string | 否 | 是否作为纯文本发送 |
| `source` | string | 否 | 合并转发来源 |
| `news` | array<object> | 否 | 合并转发新闻 |
| `summary` | string | 否 | 合并转发摘要 |
| `prompt` | string | 否 | 合并转发提示 |
| `timeout` | number | 否 | 自定义发送超时(毫秒)，覆盖自动计算值 |

**示例**

```json
{
  "group_id": "123456789",
  "messages": []
}
```

### `send_private_forward_msg`

**摘要**：发送私聊合并转发消息
**标签**：`Go-CQHTTP`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message_type` | string | 否 | 消息类型 (private/group)（可选：`private`, `group`） |
| `user_id` | string | 否 | 用户QQ |
| `group_id` | string | 否 | 群号 |
| `message` | OB11MessageMixType | 是 |  |
| `auto_escape` | boolean / string | 否 | 是否作为纯文本发送 |
| `source` | string | 否 | 合并转发来源 |
| `news` | array<object> | 否 | 合并转发新闻 |
| `summary` | string | 否 | 合并转发摘要 |
| `prompt` | string | 否 | 合并转发提示 |
| `timeout` | number | 否 | 自定义发送超时(毫秒)，覆盖自动计算值 |

**示例**

```json
{
  "user_id": "123456789",
  "messages": []
}
```

### `set_group_portrait`

**摘要**：设置群头像
**标签**：`Go-CQHTTP`

**说明**

修改指定群聊的头像

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | string | 是 | 头像文件路径或 URL |
| `group_id` | string | 是 | 群号 |

**示例**

```json
{
  "group_id": "123456",
  "file": "base64://..."
}
```

### `set_qq_profile`

**摘要**：设置QQ资料
**标签**：`Go-CQHTTP`

**说明**

修改当前账号的昵称、个性签名等资料

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `nickname` | string | 是 | 昵称 |
| `personal_note` | string | 否 | 个性签名 |
| `sex` | number / string | 否 | 性别 (0: 未知, 1: 男, 2: 女) |

**示例**

```json
{
  "nickname": "新昵称",
  "personal_note": "个性签名"
}
```

### `upload_group_file`

**摘要**：上传群文件
**标签**：`Go-CQHTTP`

**说明**

上传资源路径或URL指定的文件到指定群聊的文件系统中

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `group_id` | string | 是 | 群号 |
| `file` | string | 是 | 资源路径或URL |
| `name` | string | 是 | 文件名 |
| `folder` | string | 否 | 父目录 ID |
| `folder_id` | string | 否 | 父目录 ID (兼容性字段) |
| `upload_file` | boolean | 是 | 是否执行上传（默认 `True`） |

**示例**

```json
{
  "group_id": "123456",
  "file": "/path/to/file",
  "name": "test.txt"
}
```

### `upload_private_file`

**摘要**：上传私聊文件
**标签**：`Go-CQHTTP`

**说明**

上传本地文件到指定私聊会话中

**参数**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | string | 是 | 用户 QQ |
| `file` | string | 是 | 资源路径或URL |
| `name` | string | 是 | 文件名 |
| `upload_file` | boolean | 是 | 是否执行上传（默认 `True`） |

**示例**

```json
{
  "user_id": "123456789",
  "file": "/path/to/file",
  "name": "test.txt"
}
```

---

## 怎么查

```bash
python -m napcat_api actions --search qzone
python -m napcat_api doc send_group_msg
```
