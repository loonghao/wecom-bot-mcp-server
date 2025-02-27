# WeCom Bot MCP Server

<div align="center">
    <img src="wecom.png" alt="WeCom Bot Logo" width="200"/>
</div>

企业微信机器人 MCP 服务 - 一个遵循 Model Context Protocol (MCP) 的企业微信机器人服务器实现。

[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[English](README.md) | [中文](README_zh.md)

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

## 快速开始

### 环境要求

- Python 3.10+
- 企业微信机器人 Webhook URL

## 安装

有以下几种方式安装 WeCom Bot MCP Server：

1. 通过 [Smithery](https://smithery.ai/server/wecom-bot-mcp-server) 安装（推荐）：

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

2. 使用 VSCode 的 [Cline 插件](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)：

- 从 VSCode marketplace 安装 Cline 插件
- 打开命令面板（Ctrl+Shift+P / Cmd+Shift+P）
- 搜索 "Cline: Install Package"
- 输入 "wecom-bot-mcp-server" 并按回车

3. 手动配置：
```json
// ~/.codeium/windsurf/mcp_config.json
{
  "mcp_servers": {
    "wecom": {
      "type": "wecom-bot-server",
      "config": {
        "webhook_url": "your-webhook-url"
      }
    }
  }
}
```

### 配置

1. 设置必需的环境变量：
```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "your-webhook-url"

# 可选配置
$env:MCP_LOG_LEVEL = "DEBUG"  # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
```

2. 日志配置：
- 默认日志位置：系统日志目录下的 `mcp_wecom.log`
- 可通过 `MCP_LOG_FILE` 环境变量自定义日志位置

### 使用示例

在 MCP 环境中使用：

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

## 开发指南

### 环境准备

- Python 3.10+
- uv（Python 包管理工具）

### 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. 使用 uv 安装依赖：
```bash
uv venv
uv pip install -e ".[dev]"
```

3. 运行测试：
```bash
uvx nox -s test
```

4. 运行代码检查：
```bash
uvx nox -s lint
```

## 日志管理

日志系统使用 `platformdirs` 进行跨平台日志文件管理：

- Windows: `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\logs`
- Linux: `~/.local/share/wecom-bot-mcp-server/logs`
- macOS: `~/Library/Application Support/wecom-bot-mcp-server/logs`

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 作者：longhao
- 邮箱：hal.long@outlook.com
