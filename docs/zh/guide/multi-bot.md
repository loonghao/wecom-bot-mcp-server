# 多机器人支持

WeCom Bot MCP Server 支持配置和使用多个机器人，允许您将消息路由到不同的群组或为不同目的使用不同的机器人。

## 为什么需要多机器人？

- **职责分离**：使用不同机器人处理告警、CI/CD 通知和团队更新
- **多群组**：向不同的企业微信群组发送消息
- **访问控制**：不同团队可以有自己的机器人

## 配置方式

### 方式 1：JSON 配置（推荐）

在单个 JSON 环境变量中配置所有机器人：

::: code-group

```bash [Linux/macOS]
export WECOM_BOTS='{
  "alert": {
    "name": "告警机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "description": "用于系统告警"
  },
  "ci": {
    "name": "CI 机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy",
    "description": "用于 CI/CD 通知"
  },
  "team": {
    "name": "团队机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz",
    "description": "用于团队更新"
  }
}'
```

```powershell [Windows PowerShell]
$env:WECOM_BOTS = '{"alert": {"name": "告警机器人", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "description": "用于系统告警"}, "ci": {"name": "CI 机器人", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy", "description": "用于 CI/CD 通知"}}'
```

:::

### 方式 2：独立环境变量

为每个机器人设置单独的环境变量：

```bash
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy"
export WECOM_BOT_NOTIFY_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz"
```

机器人 ID 从变量名派生（小写）：`WECOM_BOT_ALERT_URL` → `alert`

### 方式 3：混合模式

使用 `WECOM_WEBHOOK_URL` 作为默认机器人并添加更多机器人：

```bash
# 默认机器人
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default"

# 额外机器人
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci"
```

## MCP 客户端配置

### Claude Desktop / Windsurf / Cline

```json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default",
        "WECOM_BOTS": "{\"alert\": {\"name\": \"告警机器人\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert\"}, \"ci\": {\"name\": \"CI 机器人\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci\"}}"
      }
    }
  }
}
```

## 使用多机器人

### 与 AI 助手

AI 助手会自动了解可用的机器人。您可以指定使用哪个机器人：

```
USER: "发送紧急告警到告警机器人：服务器 CPU 超过 90%"
ASSISTANT: [使用 send_message，bot_id="alert"]

USER: "发送构建成功通知到 CI 机器人"
ASSISTANT: [使用 send_message，bot_id="ci"]

USER: "有哪些企业微信机器人可用？"
ASSISTANT: [使用 list_wecom_bots 工具显示所有机器人]
```

### 使用 Python API

```python
from wecom_bot_mcp_server import send_message, send_wecom_file, send_wecom_image

# 发送到默认机器人
await send_message("你好！", msg_type="text")

# 发送到指定机器人
await send_message(
    content="⚠️ 检测到高 CPU 使用率！",
    msg_type="markdown",
    bot_id="alert"
)

# 发送文件到 CI 机器人
await send_wecom_file("/path/to/report.pdf", bot_id="ci")

# 发送图片到团队机器人
await send_wecom_image("/path/to/chart.png", bot_id="team")
```

### 列出可用机器人

```python
from wecom_bot_mcp_server.bot_config import list_available_bots, get_bot_registry

# 列出所有机器人
bots = list_available_bots()
for bot in bots:
    print(f"机器人: {bot['id']} - {bot['name']} - {bot['description']}")

# 检查机器人是否存在
registry = get_bot_registry()
if registry.has_bot("alert"):
    print("告警机器人已配置")

# 获取机器人数量
print(f"总机器人数: {registry.get_bot_count()}")
```

## 最佳实践

1. **使用描述性名称**：给机器人有意义的名称和描述
2. **职责分离**：为不同目的使用不同机器人
3. **默认机器人**：始终配置一个默认机器人用于通用消息
4. **记录机器人**：跟踪哪个机器人用于什么目的

## 故障排除

### 找不到机器人错误

如果出现 "Bot 'xxx' not found"，请检查：
1. 机器人 ID 拼写正确（不区分大小写）
2. 环境变量设置正确
3. 配置更改后重启 MCP 客户端

### 列出可用机器人

使用 `list_wecom_bots` MCP 工具或 Python API 查看所有配置的机器人：

```python
from wecom_bot_mcp_server.bot_config import list_available_bots
print(list_available_bots())
```
