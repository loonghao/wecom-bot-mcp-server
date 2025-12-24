# 多机器人配置

配置多个企业微信机器人的详细指南。

## 配置方式

### 方式 1：WECOM_BOTS JSON（推荐）

配置多个机器人最灵活的方式：

```json
{
  "bot_id": {
    "name": "显示名称",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "description": "AI 上下文的可选描述"
  }
}
```

**完整示例：**

::: code-group

```bash [Linux/macOS]
export WECOM_BOTS='{
  "default": {
    "name": "通用机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=general",
    "description": "用于一般公告"
  },
  "alert": {
    "name": "告警机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert",
    "description": "用于系统告警和紧急通知"
  },
  "ci": {
    "name": "CI/CD 机器人",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci",
    "description": "用于构建、测试和部署通知"
  },
  "team-frontend": {
    "name": "前端团队",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=frontend",
    "description": "前端团队群组"
  }
}'
```

```powershell [Windows PowerShell]
$env:WECOM_BOTS = '{"default": {"name": "通用机器人", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=general"}, "alert": {"name": "告警机器人", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"}, "ci": {"name": "CI/CD 机器人", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci"}}'
```

:::

### 方式 2：独立环境变量

对于更简单的设置或无法使用 JSON 时：

```bash
# 每个变量从变量名创建一个机器人
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci"
export WECOM_BOT_DEVOPS_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=devops"
```

**命名规则：**
- 模式：`WECOM_BOT_{NAME}_URL`
- `{NAME}` 成为机器人 ID（转换为小写）
- 示例：`WECOM_BOT_MY_TEAM_URL` → 机器人 ID：`my_team`

### 方式 3：混合配置

将 `WECOM_WEBHOOK_URL` 与其他方式混合使用：

```bash
# 这成为 "default" 机器人
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default"

# 额外机器人
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
export WECOM_BOTS='{"ci": {"name": "CI 机器人", "webhook_url": "https://..."}}'
```

## 机器人 ID 指南

- **使用小写**：机器人 ID 不区分大小写，存储为小写
- **使用描述性名称**：`alert`、`ci`、`team-frontend` 比 `bot1`、`bot2` 更好
- **避免特殊字符**：只使用字母、数字、连字符和下划线
- **保留 "default"**：未指定 `bot_id` 时使用 `default` 机器人

## AI 上下文的描述

`description` 字段帮助 AI 助手选择正确的机器人：

```json
{
  "alert": {
    "name": "告警机器人",
    "webhook_url": "https://...",
    "description": "用于系统告警、错误和紧急通知"
  },
  "ci": {
    "name": "CI 机器人",
    "webhook_url": "https://...",
    "description": "用于构建结果、测试报告和部署状态"
  }
}
```

当您要求 AI "发送构建通知"时，它会智能地选择 CI 机器人。

## 加载优先级

当同一机器人 ID 被多次定义时：

1. **WECOM_WEBHOOK_URL** → `default` 机器人（首先加载）
2. **WECOM_BOTS** → 可以覆盖 `default` 并添加更多
3. **WECOM_BOT_{NAME}_URL** → 仅在未定义时添加

## 验证

### 列出所有机器人

问 AI 助手：
```
有哪些企业微信机器人可用？
```

或使用 Python：
```python
from wecom_bot_mcp_server.bot_config import list_available_bots
print(list_available_bots())
```

### 检查特定机器人

```python
from wecom_bot_mcp_server.bot_config import get_bot_registry

registry = get_bot_registry()
if registry.has_bot("alert"):
    print("告警机器人已配置")
    print(f"URL: {registry.get_webhook_url('alert')}")
```

## 故障排除

### 找不到机器人

```
Error: Bot 'xxx' not found. Available bots: default, alert, ci
```

**解决方案：**
1. 检查机器人 ID 拼写（不区分大小写）
2. 验证环境变量已设置
3. 重启 MCP 客户端

### 无效 JSON

```
Warning: Invalid JSON in WECOM_BOTS
```

**解决方案：**
1. 使用 JSON 验证器验证 JSON
2. 检查配置文件中的正确转义
3. 在 shell 中使用单引号包裹 JSON 值

### 空 Webhook URL

```
Error: Bot 'xxx' has empty webhook_url
```

**解决方案：**
1. 检查 webhook URL 不为空
2. 验证 URL 格式正确
3. 确保 URL 中没有多余空格
