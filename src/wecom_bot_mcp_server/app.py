"""Application configuration for WeCom Bot MCP Server."""

# Import third-party modules
from mcp.server.fastmcp import FastMCP

# Constants
APP_NAME = "wecom_bot_mcp_server"
APP_DESCRIPTION = """WeCom Bot MCP Server for sending messages and files to WeCom groups.

## Mentioning Users (@Users)

When users want to mention/notify/remind specific people in messages, you MUST intelligently
convert natural language mentions to WeCom's `<@userid>` syntax.

### Automatic Mention Detection

When user says things like:
- "remind Zhang San and Li Si" → Convert to `<@zhangsan> <@lisi>` in content
- "notify @alice and @bob" → Convert to `<@alice> <@bob>` in content
- "cc wangwu, zhaoliu" → Convert to `<@wangwu> <@zhaoliu>` in content
- "let the team know" or "everyone" → Convert to `<@all>` in content
- "@all members" → Convert to `<@all>` in content

### Mention Syntax Rules

1. **For markdown messages**: Use `<@userid>` syntax DIRECTLY in the content
   - Example: "Hello <@zhangsan>, please review this!"
   - IMPORTANT: When content contains `<@userid>`, you MUST use `msg_type="markdown"`

2. **For text messages**: Use `mentioned_list` parameter
   - Example: `mentioned_list=["zhangsan", "lisi"]`

3. **User ID conventions**:
   - Convert Chinese names to pinyin: "张三" → "zhangsan", "李四" → "lisi"
   - Keep English names lowercase: "Alice" → "alice", "Bob" → "bob"
   - Preserve usernames if explicitly provided: "@zhangwei" → "zhangwei"

### Examples

User: "Send a message reminding wangwu and zhaoliu to review the PR"
→ Content: "Hi <@wangwu> <@zhaoliu>, please review the PR."
→ msg_type: "markdown" (MUST use markdown when content has <@userid>)

User: "Notify everyone about the meeting"
→ Content: "<@all> Meeting reminder: Team sync at 3 PM"
→ msg_type: "markdown"

User: "Send this to Zhang San: the report is ready"
→ Content: "Hi <@zhangsan>, the report is ready."
→ msg_type: "markdown"

## Multi-Bot Support

This server supports multiple WeCom bot configurations. You can send messages to different
bots by specifying the `bot_id` parameter in send functions.

### Checking Available Bots

Before sending messages, you can call `list_wecom_bots` to see all configured bots:
- Each bot has an `id`, `name`, and optional `description`
- The `default` bot is used when no `bot_id` is specified

### Sending to Specific Bots

When calling `send_message`, `send_wecom_image`, `send_wecom_file`, or template card tools:
- Omit `bot_id` to use the default bot
- Specify `bot_id` to target a specific bot (e.g., `bot_id="alert"` or `bot_id="ci"`)

### Configuration

Bots can be configured via environment variables:
1. `WECOM_WEBHOOK_URL` - Sets the default bot (backward compatible)
2. `WECOM_BOTS` - JSON object for multiple bots:
   `{"alert": {"name": "Alert Bot", "webhook_url": "https://..."}, ...}`
3. `WECOM_BOT_<NAME>_URL` - Individual bot URLs (e.g., `WECOM_BOT_ALERT_URL`)

### Best Practices

- Use descriptive bot names that indicate their purpose (e.g., "CI Notifications", "Alerts")
- When multiple bots are available, always consider which bot is most appropriate
- Use `list_wecom_bots` to discover available bots before sending
"""

# Initialize FastMCP server
mcp = FastMCP(
    name=APP_NAME,
    instructions=APP_DESCRIPTION,
)
