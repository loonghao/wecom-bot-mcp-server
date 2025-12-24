# 环境变量

WeCom Bot MCP Server 支持的所有环境变量完整参考。

## 机器人配置

### WECOM_WEBHOOK_URL

默认机器人的 webhook URL。这是单机器人设置的最简单配置。

```bash
# Linux/macOS
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

# Windows CMD
set WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY
```

### WECOM_BOTS

多机器人的 JSON 配置。这是配置多个机器人的推荐方式。

**格式：**
```json
{
  "bot_id": {
    "name": "可读名称",
    "webhook_url": "https://...",
    "description": "可选描述"
  }
}
```

**示例：**
```bash
export WECOM_BOTS='{
  "alert": {
    "name": "告警机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "description": "用于系统告警和通知"
  },
  "ci": {
    "name": "CI/CD 机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy",
    "description": "用于构建和部署通知"
  }
}'
```

### WECOM_BOT_\{NAME\}_URL

每个机器人的单独环境变量。机器人 ID 从变量名派生。

```bash
# 创建 id 为 "alert" 的机器人
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"

# 创建 id 为 "ci" 的机器人
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy"

# 创建 id 为 "devops" 的机器人
export WECOM_BOT_DEVOPS_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz"
```

## 日志配置

### MCP_LOG_LEVEL

设置日志详细级别。

| 值 | 描述 |
|----|------|
| `DEBUG` | 详细调试信息 |
| `INFO` | 一般操作信息（默认） |
| `WARNING` | 仅警告消息 |
| `ERROR` | 仅错误消息 |
| `CRITICAL` | 仅严重错误 |

```bash
export MCP_LOG_LEVEL="DEBUG"
```

### MCP_LOG_FILE

日志文件的自定义路径。如未设置，日志存储在平台特定目录。

```bash
export MCP_LOG_FILE="/var/log/wecom-bot/mcp.log"
```

**默认日志位置：**

| 平台 | 默认路径 |
|------|----------|
| Windows | `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\Logs\mcp_wecom.log` |
| Linux | `~/.local/state/hal/wecom-bot-mcp-server/log/mcp_wecom.log` |
| macOS | `~/Library/Logs/hal/wecom-bot-mcp-server/mcp_wecom.log` |

## 配置示例

### 单机器人设置

```bash
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
export MCP_LOG_LEVEL="INFO"
```

### 多机器人 JSON 设置

```bash
export WECOM_BOTS='{
  "default": {"name": "通用", "webhook_url": "https://...?key=default"},
  "alert": {"name": "告警", "webhook_url": "https://...?key=alert"},
  "ci": {"name": "CI/CD", "webhook_url": "https://...?key=ci"}
}'
```

### 生产环境设置

```bash
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
export MCP_LOG_LEVEL="WARNING"
export MCP_LOG_FILE="/var/log/wecom-bot/mcp.log"
```

## 验证

服务器在启动时验证所有配置：

- Webhook URL 必须以 `http://` 或 `https://` 开头
- 机器人 ID 不区分大小写（存储为小写）
- 无效配置会被记录但不会阻止启动

::: warning
如果没有找到有效的机器人配置，服务器会启动但所有消息操作都会失败。
:::
