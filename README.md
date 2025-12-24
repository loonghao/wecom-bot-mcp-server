[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/loonghao-wecom-bot-mcp-server-badge.png)](https://mseep.ai/app/loonghao-wecom-bot-mcp-server)

# WeCom Bot MCP Server

<div align="center">
    <img src="wecom.png" alt="WeCom Bot Logo" width="200"/>
</div>

A Model Context Protocol (MCP) compliant server implementation for WeCom (WeChat Work) bot.

[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![codecov](https://codecov.io/gh/loonghao/wecom-bot-mcp-server/branch/main/graph/badge.svg)](https://app.codecov.io/gh/loonghao/wecom-bot-mcp-server)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![smithery badge](https://smithery.ai/badge/wecom-bot-mcp-server)](https://smithery.ai/server/wecom-bot-mcp-server)

[English](README.md) | [中文](README_zh.md)

<a href="https://glama.ai/mcp/servers/amr2j23lbk"><img width="380" height="200" src="https://glama.ai/mcp/servers/amr2j23lbk/badge" alt="WeCom Bot Server MCP server" /></a>

## Features

- Support for multiple message types:
  - Markdown messages (with @mentions and font colors)
  - Markdown V2 messages (with tables, lists, embedded images)
  - Image messages (base64/local file/URL)
  - File messages
  - Template card messages (text_notice and news_notice)
- **Multi-bot support**: Configure and use multiple WeCom bots
- @mention support (via user ID or phone number)
- Message history tracking
- Configurable logging system
- Full type annotations
- Pydantic-based data validation

## Requirements

- Python 3.10+
- WeCom Bot Webhook URL (obtained from WeCom group settings)

## Installation

There are several ways to install WeCom Bot MCP Server:

### 1. Automated Installation (Recommended)

#### Using Smithery (For Claude Desktop):

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

#### Using VSCode with Cline Extension:

1. Install [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) from VSCode marketplace
2. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
3. Search for "Cline: Install Package"
4. Type "wecom-bot-mcp-server" and press Enter

### 2. Manual Configuration

Add the server to your MCP client configuration file:

```json
// For Claude Desktop on macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
// For Claude Desktop on Windows: %APPDATA%\Claude\claude_desktop_config.json
// For Windsurf: ~/.windsurf/config.json
// For Cline in VSCode: VSCode Settings > Cline > MCP Settings
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

## Configuration

### Setting Environment Variables

#### Single Bot (Default)

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "your-webhook-url"

# Optional configurations
$env:MCP_LOG_LEVEL = "DEBUG"  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
$env:MCP_LOG_FILE = "path/to/custom/log/file.log"  # Custom log file path
```

#### Multiple Bots Configuration

You can configure multiple bots using any of these methods:

**Method 1: JSON Configuration (Recommended)**

```bash
# Windows PowerShell
$env:WECOM_BOTS = '{"alert": {"name": "Alert Bot", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "description": "For alerts"}, "ci": {"name": "CI Bot", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy", "description": "For CI/CD"}}'

# Linux/macOS
export WECOM_BOTS='{"alert": {"name": "Alert Bot", "webhook_url": "https://...", "description": "For alerts"}, "ci": {"name": "CI Bot", "webhook_url": "https://...", "description": "For CI/CD"}}'
```

**Method 2: Individual Environment Variables**

```bash
# Windows PowerShell
$env:WECOM_BOT_ALERT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
$env:WECOM_BOT_CI_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy"
$env:WECOM_BOT_NOTIFY_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz"
```

**Method 3: Combined Mode**

```bash
# WECOM_WEBHOOK_URL becomes the "default" bot
$env:WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default"
# Additional bots
$env:WECOM_BOT_ALERT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
```

#### MCP Client Configuration with Multiple Bots

```json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default",
        "WECOM_BOTS": "{\"alert\": {\"name\": \"Alert Bot\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert\"}, \"ci\": {\"name\": \"CI Bot\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci\"}}"
      }
    }
  }
}
```

### Log Management

The logging system uses `platformdirs.user_log_dir()` for cross-platform log file management:

- Windows: `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\Logs`
- Linux: `~/.local/state/hal/wecom-bot-mcp-server/log`
- macOS: `~/Library/Logs/hal/wecom-bot-mcp-server`

The log file is named `mcp_wecom.log` and is stored in the above directory.

You can customize the log level and file path using environment variables:
- `MCP_LOG_LEVEL`: Set to DEBUG, INFO, WARNING, ERROR, or CRITICAL
- `MCP_LOG_FILE`: Set to a custom log file path

## Usage

Once configured, the MCP server runs automatically when your MCP client starts. You can interact with it through natural language in your AI assistant.

### Usage Examples

**Scenario 1: Send weather information to WeCom**
```
USER: "How's the weather in Shenzhen today? Send it to WeCom"
ASSISTANT: "I'll check Shenzhen's weather and send it to WeCom"
[The assistant will use the send_message tool to send the weather information]
```

**Scenario 2: Send meeting reminder and @mention relevant people**
```
USER: "Send a reminder for the 3 PM project review meeting, remind Zhang San and Li Si to attend"
ASSISTANT: "I'll send the meeting reminder"
[The assistant will use the send_message tool with mentioned_list parameter]
```

**Scenario 3: Send a file**
```
USER: "Send this weekly report to the WeCom group"
ASSISTANT: "I'll send the weekly report"
[The assistant will use the send_file tool]
```

**Scenario 4: Send an image**
```
USER: "Send this chart image to WeCom"
ASSISTANT: "I'll send the image"
[The assistant will use the send_image tool]
```

### Available MCP Tools

The server provides the following tools that your AI assistant can use:

1. **send_message** - Send text or markdown messages
   - Parameters: `content`, `msg_type` (markdown/markdown_v2), `mentioned_list`, `mentioned_mobile_list`, `bot_id`
   - `markdown`: Use when content contains `<@userid>` mentions or font colors. The `<@userid>` syntax is WeCom's official mention format, which avoids conflicts with email addresses like `@user@email.com`
   - `markdown_v2`: Use for tables, lists, embedded images, or general content (default)

2. **send_wecom_file** - Send files to WeCom
   - Parameters: `file_path`, `bot_id`

3. **send_wecom_image** - Send images to WeCom
   - Parameters: `image_path` (local path or URL), `bot_id`

4. **send_wecom_template_card_text_notice** - Send text notice template card
   - Parameters: `template_card_source`, `template_card_main_title`, `template_card_card_action`, `bot_id`, and optional fields
   - Use for notifications with emphasis content, quotes, and action buttons

5. **send_wecom_template_card_news_notice** - Send news notice template card
   - Parameters: `template_card_source`, `template_card_main_title`, `template_card_card_action`, `template_card_image`, `bot_id`, and optional fields
   - Use for news-style notifications with images and rich content

6. **list_wecom_bots** - List all configured bots
   - Returns: List of available bots with their IDs, names, and descriptions

### Multi-Bot Usage Examples

**Scenario 5: Send alert to specific bot**
```
USER: "Send a critical alert to the alert bot: Server CPU usage is above 90%"
ASSISTANT: "I'll send the alert to the alert bot"
[The assistant will use send_message with bot_id="alert"]
```

**Scenario 6: List available bots**
```
USER: "What WeCom bots are available?"
ASSISTANT: "Let me check the available bots"
[The assistant will use list_wecom_bots tool]
```

**Scenario 7: Send CI notification**
```
USER: "Send build success notification to the CI bot"
ASSISTANT: "I'll send the notification to the CI bot"
[The assistant will use send_message with bot_id="ci"]
```

**Scenario 8: Send template card notification**
```
USER: "Send a deployment success notification card with a link to the dashboard"
ASSISTANT: "I'll send a template card notification"
[The assistant will use send_wecom_template_card_text_notice tool]
```

**Scenario 9: Send news-style notification**
```
USER: "Send a news card about the new feature release with an image"
ASSISTANT: "I'll send a news notice card"
[The assistant will use send_wecom_template_card_news_notice tool]
```

### For Developers: Direct API Usage

If you want to use this package directly in your Python code (not as an MCP server):

```python
from wecom_bot_mcp_server import send_message, send_wecom_file, send_wecom_image, send_wecom_template_card

# Send markdown message (uses default bot)
await send_message(
    content="**Hello World!**",
    msg_type="markdown"
)

# Send markdown_v2 message with tables and lists (default)
await send_message(
    content="| Column1 | Column2 |\n|---------|---------|\\n| Value1  | Value2  |",
    msg_type="markdown_v2"
)

# Send text message and mention users (use markdown for @mentions)
await send_message(
    content="Hello <@user1> <@user2>",
    msg_type="markdown",
    mentioned_list=["user1", "user2"]
)

# Send message to a specific bot
await send_message(
    content="Build completed successfully!",
    msg_type="markdown_v2",
    bot_id="ci"  # Send to CI bot
)

# Send alert to alert bot
await send_message(
    content="⚠️ High CPU usage detected!",
    msg_type="markdown_v2",
    bot_id="alert"
)

# Send file to specific bot
await send_wecom_file("/path/to/file.txt", bot_id="ci")

# Send image to specific bot
await send_wecom_image("/path/to/image.png", bot_id="alert")

# Send template card (text_notice)
await send_wecom_template_card(
    template_card_type="text_notice",
    template_card_source={"icon_url": "https://example.com/icon.png", "desc": "System"},
    template_card_main_title={"title": "Deployment Success", "desc": "Production environment"},
    template_card_card_action={"type": 1, "url": "https://example.com/dashboard"},
    template_card_emphasis_content={"title": "100%", "desc": "Success Rate"},
    bot_id="ci"
)
```

### Multi-Bot Configuration in Code

```python
from wecom_bot_mcp_server.bot_config import get_bot_registry, list_available_bots

# List all available bots
bots = list_available_bots()
for bot in bots:
    print(f"Bot: {bot['id']} - {bot['name']}")

# Check if a specific bot exists
registry = get_bot_registry()
if registry.has_bot("alert"):
    print("Alert bot is configured")

# Get webhook URL for a specific bot
url = registry.get_webhook_url("ci")
```

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. Create a virtual environment and install dependencies:
```bash
# Using uv (recommended)
pip install uv
uv venv
uv pip install -e ".[dev]"

# Or using traditional method
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests with coverage
uvx nox -s pytest

# Run import tests only
uvx nox -s test_imports

# Run specific test file
uvx nox -s pytest -- tests/test_message.py

# Run tests with verbose output
uvx nox -s pytest -- -v
```

### Code Style

```bash
# Check code
uvx nox -s lint

# Automatically fix code style issues
uvx nox -s lint_fix
```

### Building and Publishing

```bash
# Build the package
uvx nox -s build

# Publish to PyPI (requires authentication)
uvx nox -s publish
```

### Continuous Integration

The project uses GitHub Actions for CI/CD:
- **MR Checks**: Runs on all pull requests, tests on Ubuntu, Windows, and macOS with Python 3.10, 3.11, and 3.12
- **Code Coverage**: Uploads coverage reports to Codecov
- **Import Tests**: Ensures the package can be imported correctly after installation

All dependencies are automatically tested during CI to catch issues early.

## Project Structure

```
wecom-bot-mcp-server/
├── src/
│   └── wecom_bot_mcp_server/
│       ├── __init__.py
│       ├── __main__.py
│       ├── __version__.py
│       ├── app.py           # FastMCP application setup
│       ├── server.py        # Server entry point
│       ├── message.py       # Message and template card handling
│       ├── file.py          # File upload handling
│       ├── image.py         # Image upload handling
│       ├── bot_config.py    # Multi-bot configuration
│       ├── utils.py         # Utility functions
│       ├── log_config.py    # Logging configuration
│       └── errors.py        # Error definitions
├── tests/
│   ├── test_server.py
│   ├── test_message.py
│   ├── test_file.py
│   ├── test_image.py
│   └── test_bot_config.py
├── docs/
├── pyproject.toml
├── noxfile.py
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Author: longhao
- Email: hal.long@outlook.com
