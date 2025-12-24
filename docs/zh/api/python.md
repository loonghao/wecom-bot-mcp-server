# Python API 参考

直接 Python API，用于编程访问企业微信机器人功能。

## 安装

```bash
pip install wecom-bot-mcp-server
```

## 快速开始

```python
import asyncio
from wecom_bot_mcp_server import send_message

async def main():
    await send_message("来自 Python 的问候！", msg_type="text")

asyncio.run(main())
```

## 消息函数

### send_message

发送文本或 Markdown 消息。

```python
async def send_message(
    content: str,
    msg_type: str = "text",
    mentioned_list: list[str] | None = None,
    mentioned_mobile_list: list[str] | None = None,
    bot_id: str | None = None,
) -> dict
```

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `content` | str | - | 消息内容 |
| `msg_type` | str | "text" | "text" 或 "markdown" |
| `mentioned_list` | list | None | 要 @提及的用户 ID |
| `mentioned_mobile_list` | list | None | 要 @提及的手机号 |
| `bot_id` | str | None | 目标机器人（None 则使用默认） |

**示例：**

```python
# 简单文本消息
await send_message("你好世界！")

# Markdown 消息
await send_message(
    content="**粗体** 和 *斜体*",
    msg_type="markdown"
)

# 带 @提及
await send_message(
    content="请审核这个",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)

# 通过手机号提及
await send_message(
    content="紧急！",
    msg_type="text",
    mentioned_mobile_list=["13800138000"]
)

# 提及所有人
await send_message(
    content="团队公告",
    msg_type="text",
    mentioned_list=["@all"]
)

# 发送到指定机器人
await send_message(
    content="构建失败！",
    msg_type="markdown",
    bot_id="ci"
)
```

### send_wecom_file

向企业微信发送文件。

```python
async def send_wecom_file(
    file_path: str,
    bot_id: str | None = None,
) -> dict
```

**示例：**

```python
# 发送文件
await send_wecom_file("/path/to/report.pdf")

# 发送到指定机器人
await send_wecom_file("/path/to/build.log", bot_id="ci")
```

### send_wecom_image

向企业微信发送图片。

```python
async def send_wecom_image(
    image_path: str,
    bot_id: str | None = None,
) -> dict
```

**示例：**

```python
# 发送本地图片
await send_wecom_image("/path/to/chart.png")

# 从 URL 发送
await send_wecom_image("https://example.com/image.png")

# 发送到指定机器人
await send_wecom_image("/path/to/screenshot.png", bot_id="alert")
```

## 机器人管理

### get_bot_registry

获取全局机器人注册表实例。

```python
from wecom_bot_mcp_server.bot_config import get_bot_registry

registry = get_bot_registry()
```

**方法：**

```python
# 按 ID 获取机器人
bot = registry.get("alert")  # 返回 BotConfig
bot = registry.get()  # 返回默认机器人

# 获取 webhook URL
url = registry.get_webhook_url("alert")
url = registry.get_webhook_url()  # 默认机器人 URL

# 列出所有机器人
bots = registry.list_bots()  # 返回字典列表

# 检查机器人是否存在
exists = registry.has_bot("alert")  # 返回 bool

# 检查是否有多个机器人
multiple = registry.has_multiple_bots()  # 返回 bool

# 获取机器人数量
count = registry.get_bot_count()  # 返回 int

# 重新加载配置
registry.reload()  # 重新读取环境变量
```

### list_available_bots

列出所有配置的机器人。

```python
from wecom_bot_mcp_server.bot_config import list_available_bots

bots = list_available_bots()
# 返回: [{"id": "default", "name": "默认", "description": "...", "has_webhook": True}, ...]
```

## 错误处理

```python
from wecom_bot_mcp_server.errors import WeComError, ErrorCode

try:
    await send_message("你好", bot_id="nonexistent")
except WeComError as e:
    print(f"错误: {e.message}")
    print(f"代码: {e.error_code}")
```

## 完整示例

```python
import asyncio
import os
from wecom_bot_mcp_server import send_message, send_wecom_file, send_wecom_image
from wecom_bot_mcp_server.bot_config import get_bot_registry, list_available_bots
from wecom_bot_mcp_server.errors import WeComError

# 设置环境变量
os.environ["WECOM_WEBHOOK_URL"] = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
os.environ["WECOM_BOT_ALERT_URL"] = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"

async def main():
    # 列出可用机器人
    bots = list_available_bots()
    print(f"可用机器人: {[b['id'] for b in bots]}")

    # 发送消息
    try:
        # 文本消息到默认机器人
        await send_message("日报已准备好", msg_type="text")

        # Markdown 到 CI 机器人
        await send_message(
            content="## 构建状态\n- **结果**: 成功\n- **耗时**: 5分30秒",
            msg_type="markdown",
            bot_id="ci"
        )

        # 带 @提及的告警
        await send_message(
            content="服务器 CPU > 90%！",
            msg_type="text",
            mentioned_list=["admin"],
            bot_id="alert"
        )

        # 发送文件
        await send_wecom_file("/path/to/report.pdf")

        # 发送图片
        await send_wecom_image("/path/to/chart.png", bot_id="alert")

    except WeComError as e:
        print(f"失败: {e.message}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 类型提示

该库完全支持类型。IDE 支持：

```python
from wecom_bot_mcp_server import send_message
from wecom_bot_mcp_server.bot_config import BotConfig, BotRegistry

# 您的 IDE 将提供完整的自动补全和类型检查
```
