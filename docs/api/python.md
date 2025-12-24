# Python API Reference

Direct Python API for programmatic access to WeCom Bot functionality.

## Installation

```bash
pip install wecom-bot-mcp-server
```

## Quick Start

```python
import asyncio
from wecom_bot_mcp_server import send_message

async def main():
    await send_message("Hello from Python!", msg_type="text")

asyncio.run(main())
```

## Message Functions

### send_message

Send text or markdown messages.

```python
async def send_message(
    content: str,
    msg_type: str = "text",
    mentioned_list: list[str] | None = None,
    mentioned_mobile_list: list[str] | None = None,
    bot_id: str | None = None,
) -> dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | str | - | Message content |
| `msg_type` | str | "text" | "text" or "markdown" |
| `mentioned_list` | list | None | User IDs to @mention |
| `mentioned_mobile_list` | list | None | Phone numbers to @mention |
| `bot_id` | str | None | Target bot (uses default if None) |

**Examples:**

```python
# Simple text message
await send_message("Hello World!")

# Markdown message
await send_message(
    content="**Bold** and *italic*",
    msg_type="markdown"
)

# With @mentions
await send_message(
    content="Please review this",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)

# Mention by phone
await send_message(
    content="Urgent!",
    msg_type="text",
    mentioned_mobile_list=["13800138000"]
)

# Mention all
await send_message(
    content="Team announcement",
    msg_type="text",
    mentioned_list=["@all"]
)

# Send to specific bot
await send_message(
    content="Build failed!",
    msg_type="markdown",
    bot_id="ci"
)
```

### send_wecom_file

Send files to WeCom.

```python
async def send_wecom_file(
    file_path: str,
    bot_id: str | None = None,
) -> dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | str | - | Path to the file |
| `bot_id` | str | None | Target bot |

**Examples:**

```python
# Send a file
await send_wecom_file("/path/to/report.pdf")

# Send to specific bot
await send_wecom_file("/path/to/build.log", bot_id="ci")
```

### send_wecom_image

Send images to WeCom.

```python
async def send_wecom_image(
    image_path: str,
    bot_id: str | None = None,
) -> dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image_path` | str | - | Local path or URL |
| `bot_id` | str | None | Target bot |

**Examples:**

```python
# Send local image
await send_wecom_image("/path/to/chart.png")

# Send from URL
await send_wecom_image("https://example.com/image.png")

# Send to specific bot
await send_wecom_image("/path/to/screenshot.png", bot_id="alert")
```

## Bot Management

### get_bot_registry

Get the global bot registry instance.

```python
from wecom_bot_mcp_server.bot_config import get_bot_registry

registry = get_bot_registry()
```

**Methods:**

```python
# Get a bot by ID
bot = registry.get("alert")  # Returns BotConfig
bot = registry.get()  # Returns default bot

# Get webhook URL
url = registry.get_webhook_url("alert")
url = registry.get_webhook_url()  # Default bot URL

# List all bots
bots = registry.list_bots()  # Returns list of dicts

# Check if bot exists
exists = registry.has_bot("alert")  # Returns bool

# Check for multiple bots
multiple = registry.has_multiple_bots()  # Returns bool

# Get bot count
count = registry.get_bot_count()  # Returns int

# Reload configuration
registry.reload()  # Re-reads environment variables
```

### list_available_bots

List all configured bots.

```python
from wecom_bot_mcp_server.bot_config import list_available_bots

bots = list_available_bots()
# Returns: [{"id": "default", "name": "Default", "description": "...", "has_webhook": True}, ...]
```

### BotConfig

Data class for bot configuration.

```python
from wecom_bot_mcp_server.bot_config import BotConfig

@dataclass
class BotConfig:
    name: str           # Human-readable name
    webhook_url: str    # Webhook URL
    description: str    # Optional description
    metadata: dict      # Optional metadata
```

## Error Handling

```python
from wecom_bot_mcp_server.errors import WeComError, ErrorCode

try:
    await send_message("Hello", bot_id="nonexistent")
except WeComError as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.error_code}")
```

**Error Codes:**

```python
class ErrorCode:
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NETWORK_ERROR = "NETWORK_ERROR"
    API_ERROR = "API_ERROR"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
```

## Complete Example

```python
import asyncio
import os
from wecom_bot_mcp_server import send_message, send_wecom_file, send_wecom_image
from wecom_bot_mcp_server.bot_config import get_bot_registry, list_available_bots
from wecom_bot_mcp_server.errors import WeComError

# Set environment variables
os.environ["WECOM_WEBHOOK_URL"] = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
os.environ["WECOM_BOT_ALERT_URL"] = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"

async def main():
    # List available bots
    bots = list_available_bots()
    print(f"Available bots: {[b['id'] for b in bots]}")

    # Send messages
    try:
        # Text message to default bot
        await send_message("Daily report ready", msg_type="text")

        # Markdown to CI bot
        await send_message(
            content="## Build Status\n- **Result**: Success\n- **Duration**: 5m 30s",
            msg_type="markdown",
            bot_id="ci"
        )

        # Alert with @mention
        await send_message(
            content="Server CPU > 90%!",
            msg_type="text",
            mentioned_list=["admin"],
            bot_id="alert"
        )

        # Send file
        await send_wecom_file("/path/to/report.pdf")

        # Send image
        await send_wecom_image("/path/to/chart.png", bot_id="alert")

    except WeComError as e:
        print(f"Failed: {e.message}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Type Hints

The library is fully typed. For IDE support:

```python
from wecom_bot_mcp_server import send_message
from wecom_bot_mcp_server.bot_config import BotConfig, BotRegistry

# Your IDE will provide full autocomplete and type checking
```
