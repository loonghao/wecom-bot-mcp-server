# WeCom Bot MCP Server

<div align="center">
    <img src="wecom.png" alt="WeCom Bot Logo" width="200"/>
</div>

企业微信机器人 MCP 服务 - 一个遵循 Model Context Protocol (MCP) 的企业微信机器人服务器实现。

[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
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

### 2. 手动安装

#### 从 PyPI 安装：

```bash
pip install wecom-bot-mcp-server
```

#### 手动配置 MCP：

创建或更新 MCP 配置文件：

```json
// Windsurf 配置: ~/.windsurf/config.json
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

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "your-webhook-url"

# 可选配置
$env:MCP_LOG_LEVEL = "DEBUG"  # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
$env:MCP_LOG_FILE = "path/to/custom/log/file.log"  # 自定义日志文件路径
```

### 日志管理

日志系统使用 `platformdirs` 进行跨平台日志文件管理：

- Windows: `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\logs`
- Linux: `~/.local/share/wecom-bot-mcp-server/logs`
- macOS: `~/Library/Application Support/wecom-bot-mcp-server/logs`

## 使用

### 启动服务器

```bash
wecom-bot-mcp-server
```

### 使用示例（在 MCP 环境中）

```python
# 场景一：发送天气信息到企业微信
USER: "深圳今天天气怎么样？发送到企业微信"
ASSISTANT: "我会查询深圳天气并发送到企业微信"

await mcp.send_message(
    content="深圳天气：\n- 温度：25°C\n- 天气：晴\n- 空气质量：优",
    msg_type="markdown"
)

# 场景二：发送会议提醒并@相关人员
USER: "帮我发送下午3点的项目评审会议提醒，提醒张三和李四参加"
ASSISTANT: "好的，我来发送会议提醒"

await mcp.send_message(
    content="## 项目评审会议提醒\n\n时间：今天下午 3:00\n地点：会议室 A\n\n请准时参加！",
    msg_type="markdown",
    mentioned_list=["zhangsan", "lisi"]
)

# 场景三：发送文件
USER: "把这份周报发送到企业微信群"
ASSISTANT: "好的，我来发送周报"

await mcp.send_message(
    content=Path("weekly_report.docx"),
    msg_type="file"
)
```

### 直接 API 使用

#### 发送消息

```python
from wecom_bot_mcp_server import mcp

# 发送 markdown 消息
await mcp.send_message(
    content="**Hello World!**", 
    msg_type="markdown"
)

# 发送文本消息并提及用户
await mcp.send_message(
    content="Hello @user1 @user2",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)
```

#### 发送文件

```python
from wecom_bot_mcp_server import send_wecom_file

# 发送文件
await send_wecom_file("/path/to/file.txt")
```

#### 发送图片

```python
from wecom_bot_mcp_server import send_wecom_image

# 发送本地图片
await send_wecom_image("/path/to/image.png")

# 发送 URL 图片
await send_wecom_image("https://example.com/image.png")
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
# 使用 uv (推荐)
uvx nox -s pytest

# 或者使用传统方式
nox -s pytest
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
uv build

# 构建并发布到 PyPI
uv build && twine upload dist/*
```

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
