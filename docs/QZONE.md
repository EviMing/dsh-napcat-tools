# QQ 空间接口

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

## 空友爱看：另一套公开动态

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

---

## 注意

- `tid` 与 `feed_ref` 是两种互斥的定位方式，不能混用。
- `pos`/`num` 与 `cursor` 也不能混用；native 模式不接受 `page_num`/`count`。
- 返回里的 `html` 字段可能非常大，程序化处理时优先取 `content`、`tid`、`comments` 等结构化字段。
- 写操作没有二次确认，调用前确认 `target_uin`、`tid` 和权限参数。
