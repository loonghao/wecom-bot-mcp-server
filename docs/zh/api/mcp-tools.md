# MCP 工具参考

使用 WeCom Bot MCP Server 时，AI 助手可以使用这些工具。

## send_message

向企业微信发送文本或 Markdown 消息。

### 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `content` | string | 是 | 消息内容 |
| `msg_type` | string | 否 | 消息类型：`text`（默认）或 `markdown` |
| `mentioned_list` | array | 否 | 要 @提及的用户 ID 列表 |
| `mentioned_mobile_list` | array | 否 | 要 @提及的手机号列表 |
| `bot_id` | string | 否 | 目标机器人 ID（未指定则使用默认） |

### 示例

**简单文本消息：**
```
发送 "大家好！" 到企业微信
```

**Markdown 消息：**
```
发送一条 Markdown 消息到企业微信，包含构建状态
```

**带 @提及：**
```
发送提醒到企业微信，并提及 user1 和 user2
```

**到指定机器人：**
```
发送告警到告警机器人：服务器宕机了！
```

### 响应

```json
{
  "status": "success",
  "message": "消息发送成功",
  "bot_id": "default"
}
```

## send_wecom_file

向企业微信发送文件。

### 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `file_path` | string | 是 | 文件路径 |
| `bot_id` | string | 否 | 目标机器人 ID |

### 示例

**发送文件：**
```
把 /path/to/report.pdf 文件发送到企业微信
```

**发送到指定机器人：**
```
把构建日志发送到 CI 机器人
```

### 限制

- 最大文件大小：20MB
- 支持所有文件类型

## send_wecom_image

向企业微信发送图片。

### 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `image_path` | string | 是 | 图片文件路径或 URL |
| `bot_id` | string | 否 | 目标机器人 ID |

### 示例

**发送本地图片：**
```
把 /path/to/chart.png 图片发送到企业微信
```

**从 URL 发送：**
```
把这个图片发送到企业微信：https://example.com/image.png
```

### 限制

- 最大大小：2MB
- 支持格式：PNG、JPG、JPEG、GIF（静态）
- 超过大小限制的图片会自动压缩

## list_wecom_bots

列出所有配置的企业微信机器人。

### 参数

无

### 示例

```
有哪些企业微信机器人可用？
```

```
列出所有配置的机器人
```

### 响应

```json
{
  "bots": [
    {
      "id": "default",
      "name": "默认机器人",
      "description": "默认机器人（来自 WECOM_WEBHOOK_URL）",
      "has_webhook": true
    },
    {
      "id": "alert",
      "name": "告警机器人",
      "description": "用于系统告警",
      "has_webhook": true
    }
  ],
  "count": 2
}
```

## 错误处理

所有工具以一致的格式返回错误：

```json
{
  "status": "error",
  "error": "错误消息",
  "error_code": "VALIDATION_ERROR"
}
```

### 常见错误代码

| 代码 | 描述 |
|------|------|
| `VALIDATION_ERROR` | 无效参数 |
| `NETWORK_ERROR` | 网络连接失败 |
| `API_ERROR` | 企业微信 API 返回错误 |
| `FILE_NOT_FOUND` | 文件不存在 |
| `FILE_TOO_LARGE` | 文件超过大小限制 |

## AI 助手使用提示

1. **默认机器人**：如果用户未指定机器人，使用默认机器人
2. **机器人选择**：需要时使用 `list_wecom_bots` 查找可用机器人
3. **消息类型**：格式化内容使用 `markdown`，带 @提及的简单消息使用 `text`
4. **文件路径**：接受绝对路径和相对路径
5. **错误恢复**：如果找不到机器人，列出可用机器人并请用户选择
