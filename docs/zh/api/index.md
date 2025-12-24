# API 参考

WeCom Bot MCP Server 提供两种与企业微信交互的方式：

1. **MCP 工具** - 用于 AI 助手（Claude、Cline 等）
2. **Python API** - 用于直接编程访问

## MCP 工具

作为 MCP 服务器使用时，以下工具可供 AI 助手使用：

| 工具 | 描述 |
|------|------|
| `send_message` | 发送文本或 Markdown 消息 |
| `send_wecom_file` | 发送文件 |
| `send_wecom_image` | 发送图片 |
| `list_wecom_bots` | 列出配置的机器人 |

[查看 MCP 工具参考 →](./mcp-tools)

## Python API

直接 Python 使用：

```python
from wecom_bot_mcp_server import (
    send_message,
    send_wecom_file,
    send_wecom_image,
)
from wecom_bot_mcp_server.bot_config import (
    get_bot_registry,
    list_available_bots,
)
```

[查看 Python API 参考 →](./python)

## 快速示例

### 发送消息（MCP）

问 AI 助手：
```
发送 "Hello World!" 到企业微信
```

### 发送消息（Python）

```python
await send_message("Hello World!", msg_type="text")
```

### 发送到指定机器人

```python
await send_message("告警！", msg_type="text", bot_id="alert")
```
