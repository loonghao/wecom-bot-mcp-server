# WeCom Bot MCP Server

<div align="center">
    <img src="wecom.png" alt="WeCom Bot Logo" width="200"/>
</div>

企业微信机器人 MCP 服务 - 一个遵循 Model Context Protocol (MCP) 的企业微信机器人服务器实现。

[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![codecov](https://codecov.io/gh/loonghao/wecom-bot-mcp-server/branch/main/graph/badge.svg)](https://app.codecov.io/gh/loonghao/wecom-bot-mcp-server)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![smithery badge](https://smithery.ai/badge/wecom-bot-mcp-server)](https://smithery.ai/server/wecom-bot-mcp-server)

[English](README.md) | [中文](README_zh.md)

<a href="https://glama.ai/mcp/servers/amr2j23lbk"><img width="380" height="200" src="https://glama.ai/mcp/servers/amr2j23lbk/badge" alt="WeCom Bot Server MCP server" /></a>

## 功能特点

- 支持多种消息类型：
  - 文本消息
  - Markdown 消息
  - 图片消息（base64）
  - 文件消息
- **多机器人支持**：配置和使用多个企业微信机器人
- 支持@用户（通过用户ID或手机号）
- 消息历史记录
- 可配置的日志系统
- 完全类型注解
- 基于 Pydantic 的数据验证

## 环境要求

- Python 3.10+
- 企业微信机器人 Webhook URL（从企业微信群组设置中获取）

## 安装

有以下几种方式安装 WeCom Bot MCP Server：

### 1. 自动安装（推荐）

#### 使用 Smithery（适用于 Claude Desktop）：

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

#### 使用 VSCode 的 Cline 插件：

1. 从 VSCode marketplace 安装 [Cline 插件](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. 打开命令面板（Ctrl+Shift+P / Cmd+Shift+P）
3. 搜索 "Cline: Install Package"
4. 输入 "wecom-bot-mcp-server" 并按回车

### 2. 手动配置

将服务器添加到你的 MCP 客户端配置文件中：

```json
// Claude Desktop macOS 配置: ~/Library/Application Support/Claude/claude_desktop_config.json
// Claude Desktop Windows 配置: %APPDATA%\Claude\claude_desktop_config.json
// Windsurf 配置: ~/.windsurf/config.json
// VSCode 中的 Cline: VSCode 设置 > Cline > MCP Settings
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": [
        "wecom-bot-mcp-server"
      ],
      "env": {
        "WECOM_WEBHOOK_URL": "your-webhook-url"
      }
    }
  }
}
```

## 配置

### 设置环境变量

#### 单机器人（默认）

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "your-webhook-url"

# 可选配置
$env:MCP_LOG_LEVEL = "DEBUG"  # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
$env:MCP_LOG_FILE = "path/to/custom/log/file.log"  # 自定义日志文件路径
```

#### 多机器人配置

你可以使用以下任一方式配置多个机器人：

**方式 1：JSON 配置（推荐）**

```bash
# Windows PowerShell
$env:WECOM_BOTS = '{"alert": {"name": "告警机器人", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "description": "用于告警通知"}, "ci": {"name": "CI机器人", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy", "description": "用于CI/CD通知"}}'

# Linux/macOS
export WECOM_BOTS='{"alert": {"name": "告警机器人", "webhook_url": "https://...", "description": "用于告警通知"}, "ci": {"name": "CI机器人", "webhook_url": "https://...", "description": "用于CI/CD通知"}}'
```

**方式 2：独立环境变量**

```bash
# Windows PowerShell
$env:WECOM_BOT_ALERT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
$env:WECOM_BOT_CI_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy"
$env:WECOM_BOT_NOTIFY_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz"
```

**方式 3：混合模式**

```bash
# WECOM_WEBHOOK_URL 成为 "default" 机器人
$env:WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default"
# 额外的机器人
$env:WECOM_BOT_ALERT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
```

#### 多机器人 MCP 客户端配置

```json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default",
        "WECOM_BOTS": "{\"alert\": {\"name\": \"告警机器人\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert\"}, \"ci\": {\"name\": \"CI机器人\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci\"}}"
      }
    }
  }
}
```

### 日志管理

日志系统使用 `platformdirs.user_log_dir()` 进行跨平台日志文件管理：

- Windows: `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\Logs`
- Linux: `~/.local/state/hal/wecom-bot-mcp-server/log`
- macOS: `~/Library/Logs/hal/wecom-bot-mcp-server`

日志文件名为 `mcp_wecom.log`，存储在上述目录中。

你可以使用环境变量自定义日志级别和文件路径：
- `MCP_LOG_LEVEL`: 设置为 DEBUG、INFO、WARNING、ERROR 或 CRITICAL
- `MCP_LOG_FILE`: 设置为自定义日志文件路径

## 使用

配置完成后，MCP 服务器会在你的 MCP 客户端启动时自动运行。你可以通过自然语言与 AI 助手交互来使用它。

### 使用示例

**场景一：发送天气信息到企业微信**
```
USER: "深圳今天天气怎么样？发送到企业微信"
ASSISTANT: "我会查询深圳天气并发送到企业微信"
[助手将使用 send_message 工具发送天气信息]
```

**场景二：发送会议提醒并@相关人员**
```
USER: "帮我发送下午3点的项目评审会议提醒，提醒张三和李四参加"
ASSISTANT: "好的，我来发送会议提醒"
[助手将使用 send_message 工具，并使用 mentioned_list 参数]
```

**场景三：发送文件**
```
USER: "把这份周报发送到企业微信群"
ASSISTANT: "好的，我来发送周报"
[助手将使用 send_file 工具]
```

**场景四：发送图片**
```
USER: "把这个图表发送到企业微信"
ASSISTANT: "好的，我来发送图片"
[助手将使用 send_image 工具]
```

### 可用的 MCP 工具

服务器提供以下工具供 AI 助手使用：

1. **send_message** - 发送文本或 Markdown 消息
   - 参数：`content`、`msg_type`（text/markdown）、`mentioned_list`、`mentioned_mobile_list`、`bot_id`

2. **send_file** - 发送文件到企业微信
   - 参数：`file_path`、`bot_id`

3. **send_image** - 发送图片到企业微信
   - 参数：`image_path`（本地路径或 URL）、`bot_id`

4. **list_wecom_bots** - 列出所有已配置的机器人
   - 返回：可用机器人列表，包含 ID、名称和描述

### 多机器人使用示例

**场景五：发送告警到指定机器人**
```
USER: "发送一条紧急告警到告警机器人：服务器 CPU 使用率超过 90%"
ASSISTANT: "好的，我会发送告警到告警机器人"
[助手将使用 send_message 并设置 bot_id="alert"]
```

**场景六：列出可用机器人**
```
USER: "有哪些企业微信机器人可用？"
ASSISTANT: "让我查看可用的机器人"
[助手将使用 list_wecom_bots 工具]
```

**场景七：发送 CI 通知**
```
USER: "发送构建成功通知到 CI 机器人"
ASSISTANT: "好的，我会发送通知到 CI 机器人"
[助手将使用 send_message 并设置 bot_id="ci"]
```

### 开发者：直接 API 使用

如果你想在 Python 代码中直接使用此包（而不是作为 MCP 服务器）：

```python
from wecom_bot_mcp_server import send_message, send_wecom_file, send_wecom_image

# 发送 markdown 消息（使用默认机器人）
await send_message(
    content="**Hello World!**",
    msg_type="markdown"
)

# 发送文本消息并提及用户
await send_message(
    content="Hello @user1 @user2",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)

# 发送消息到指定机器人
await send_message(
    content="构建成功完成！",
    msg_type="markdown",
    bot_id="ci"  # 发送到 CI 机器人
)

# 发送告警到告警机器人
await send_message(
    content="⚠️ 检测到高 CPU 使用率！",
    msg_type="markdown",
    bot_id="alert"
)

# 发送文件到指定机器人
await send_wecom_file("/path/to/file.txt", bot_id="ci")

# 发送图片到指定机器人
await send_wecom_image("/path/to/image.png", bot_id="alert")
```

### 代码中的多机器人配置

```python
from wecom_bot_mcp_server.bot_config import get_bot_registry, list_available_bots

# 列出所有可用机器人
bots = list_available_bots()
for bot in bots:
    print(f"机器人: {bot['id']} - {bot['name']}")

# 检查特定机器人是否存在
registry = get_bot_registry()
if registry.has_bot("alert"):
    print("告警机器人已配置")

# 获取特定机器人的 webhook URL
url = registry.get_webhook_url("ci")
```

## 开发

### 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. 创建虚拟环境并安装依赖：
```bash
# 使用 uv (推荐)
pip install uv
uv venv
uv pip install -e ".[dev]"

# 或者使用传统方式
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 测试

```bash
# 运行所有测试并生成覆盖率报告
uvx nox -s pytest

# 仅运行导入测试
uvx nox -s test_imports

# 运行特定测试文件
uvx nox -s pytest -- tests/test_message.py

# 运行测试并显示详细输出
uvx nox -s pytest -- -v
```

### 代码风格

```bash
# 检查代码
uvx nox -s lint

# 自动修复代码风格问题
uvx nox -s lint_fix
```

### 构建和发布

```bash
# 构建包
uvx nox -s build

# 发布到 PyPI（需要认证）
uvx nox -s publish
```

### 持续集成

项目使用 GitHub Actions 进行 CI/CD：
- **MR 检查**：在所有 Pull Request 上运行，在 Ubuntu、Windows 和 macOS 上使用 Python 3.10、3.11 和 3.12 进行测试
- **代码覆盖率**：上传覆盖率报告到 Codecov
- **导入测试**：确保包在安装后能够正确导入

所有依赖项在 CI 期间自动测试，以便及早发现问题。

## 项目结构

```
wecom-bot-mcp-server/
├── src/
│   └── wecom_bot_mcp_server/
│       ├── __init__.py
│       ├── server.py
│       ├── message.py
│       ├── file.py
│       ├── image.py
│       ├── bot_config.py   # 多机器人配置
│       ├── utils.py
│       └── errors.py
├── tests/
│   ├── test_server.py
│   ├── test_message.py
│   ├── test_file.py
│   └── test_image.py
├── docs/
├── pyproject.toml
├── noxfile.py
└── README.md
```

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 作者：longhao
- 邮箱：hal.long@outlook.com
