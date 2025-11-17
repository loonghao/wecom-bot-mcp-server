"""Message handling functionality for WeCom Bot MCP Server."""

# Import built-in modules
from typing import Annotated
from typing import Any

# Import third-party modules
from loguru import logger
from mcp.server.fastmcp import Context
from notify_bridge import NotifyBridge
from pydantic import Field

# Import local modules
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.utils import encode_text
from wecom_bot_mcp_server.utils import get_webhook_url

# Constants
MESSAGE_HISTORY_KEY = "history://messages"
MARKDOWN_CAPABILITIES_RESOURCE_KEY = "wecom://markdown-capabilities"

# Message history storage
message_history: list[dict[str, str]] = []


@mcp.resource(MESSAGE_HISTORY_KEY)
def get_message_history_resource() -> str:
    """Resource endpoint to access message history.

    Returns:
        str: Formatted message history

    """
    return get_formatted_message_history()


def get_formatted_message_history() -> str:
    """Get formatted message history.

    Returns:
        str: Formatted message history as markdown

    """
    if not message_history:
        return "No message history available."

    formatted_history = "# Message History\n\n"
    for idx, msg in enumerate(message_history, 1):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        formatted_history += f"## {idx}. {role.capitalize()}\n\n{content}\n\n---\n\n"

    return formatted_history


@mcp.resource(MARKDOWN_CAPABILITIES_RESOURCE_KEY)
def get_markdown_capabilities_resource() -> str:
    """Resource endpoint describing WeCom markdown capabilities.

    This can be used by MCP clients or models to decide which message type to use
    based on the desired formatting (tables, images, colors, mentions, etc.).
    """
    return (
        "# WeCom Markdown Capabilities\n\n"
        "## Common to markdown and markdown_v2\n"
        "- Headers (# to ######)\n"
        "- Bold (**text**) and italic (*text*)\n"
        "- Links: [text](url)\n"
        "- Inline code: `code`\n"
        "- Block quotes: > quote\n\n"
        "## Only markdown\n"
        '- Font colors: <font color="info|comment|warning">text</font>\n'
        "- Mentions: <@userid>\n\n"
        "## Only markdown_v2\n"
        "- Tables (using | columns | and separator rows)\n"
        "- Lists (ordered and unordered)\n"
        "- Multi-level quotes (>>, >>>)\n"
        "- Images embedded with ![alt](url)\n"
        "- Horizontal rules (---)\n\n"
        "## Image sending recommendations\n"
        "- If the main content is a standalone image file or screenshot, "
        "send it with the send_wecom_image tool (msg_type=image).\n"
        "- If the image is just an illustration inside a larger report, "
        "use markdown_v2 and embed it with ![alt](url).\n"
    )


@mcp.prompt(title="WeCom Message Guidelines")
def wecom_message_guidelines() -> str:
    """High-level guidelines for planning WeCom messages.

    This prompt explains how to use the single supported message type
    `markdown_v2` and when to call the image/file tools.
    """
    return (
        "When sending messages to WeCom via this MCP server, follow these rules:\n\n"
        "- This server **only** supports the `markdown_v2` message type.\n"
        "- For plain text, still use `markdown_v2` but avoid extra formatting.\n"
        "- For formatted content (headings, bold/italic, links, tables, lists, images, nested quotes), "
        "also use `markdown_v2`.\n"
        "- Do not request `text` or legacy `markdown` msg_type; they will be rejected as invalid.\n"
        "- If the main content is an image file (local path or URL), "
        "call the `send_wecom_image` tool instead of embedding it in markdown.\n"
        "- URLs must be preserved exactly; do not change underscores or other "
        "characters inside URLs.\n"
    )


async def send_message(
    content: str,
    msg_type: str = "markdown_v2",
    mentioned_list: list[str] | None = None,
    mentioned_mobile_list: list[str] | None = None,
    ctx: Context | None = None,
) -> dict[str, str]:
    """Send message to WeCom.

    Args:
        content: Message content
        msg_type: Message type (only 'markdown_v2' is supported); default is markdown_v2
        mentioned_list: List of mentioned users
        mentioned_mobile_list: List of mentioned mobile numbers
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If message sending fails

    """
    if ctx:
        await ctx.report_progress(0.1)
        await ctx.info(f"Sending {msg_type} message")

    try:
        # Validate inputs
        await _validate_message_inputs(content, msg_type, ctx)

        # Get webhook URL and prepare message
        base_url = await _get_webhook_url(ctx)
        fixed_content = await _prepare_message_content(content, ctx, msg_type)

        # Add message to history
        message_history.append({"role": "assistant", "content": content})

        if ctx:
            await ctx.report_progress(0.5)
            await ctx.info("Sending message...")

        # Send message to WeCom
        response = await _send_message_to_wecom(
            base_url, msg_type, fixed_content, mentioned_list, mentioned_mobile_list
        )

        # Process response
        return await _process_message_response(response, ctx)

    except Exception as e:
        error_msg = f"Error sending message: {e!s}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.NETWORK_ERROR) from e


async def _validate_message_inputs(content: str, msg_type: str, ctx: Context | None = None) -> None:
    """Validate message inputs.

    Args:
        content: Message content
        msg_type: Message type
        ctx: FastMCP context

    Raises:
        WeComError: If validation fails

    """
    if not content:
        error_msg = "Message content cannot be empty"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.VALIDATION_ERROR)

    # Validate message type - only markdown_v2 is supported now
    if msg_type != "markdown_v2":
        error_msg = f"Invalid message type: {msg_type}. Only 'markdown_v2' is supported."
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.VALIDATION_ERROR)


async def _get_webhook_url(ctx: Context | None = None) -> str:
    """Get webhook URL.

    Args:
        ctx: FastMCP context

    Returns:
        str: Webhook URL

    Raises:
        WeComError: If webhook URL is not found

    """
    try:
        return get_webhook_url()
    except WeComError as e:
        if ctx:
            await ctx.error(str(e))
        raise


async def _prepare_message_content(content: str, ctx: Context | None = None, msg_type: str = "markdown_v2") -> str:
    """Prepare message content for sending.

    Args:
        content: Message content
        ctx: FastMCP context
        msg_type: Message type (only 'markdown_v2' is supported)

    Returns:
        str: Encoded message content

    Raises:
        WeComError: If text encoding fails

    """
    try:
        fixed_content = encode_text(content, msg_type)
        logger.info(f"Sending message: {fixed_content}")
        return fixed_content
    except ValueError as e:
        logger.error(f"Text encoding error: {e}")
        if ctx:
            await ctx.error(f"Text encoding error: {e}")
        raise WeComError(f"Text encoding error: {e}", ErrorCode.VALIDATION_ERROR) from e


async def _send_message_to_wecom(
    base_url: str,
    msg_type: str,
    content: str,
    mentioned_list: list[str] | None = None,
    mentioned_mobile_list: list[str] | None = None,
) -> Any:
    """Send message to WeCom using NotifyBridge.

    This uses the latest NotifyBridge wecom interface, which expects
    keyword arguments rather than a payload dict. The semantics of
    ``msg_type`` (currently only "markdown_v2" is supported here)
    are implemented inside NotifyBridge.

    Args:
        base_url: Webhook URL
        msg_type: Message type
        content: Message content
        mentioned_list: List of mentioned users
        mentioned_mobile_list: List of mentioned mobile numbers

    Returns:
        Any: Response from NotifyBridge

    Raises:
        WeComError: If URL is invalid or request fails

    """
    # Validate base_url format again before sending
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        error_msg = f"Invalid webhook URL format: '{base_url}'. URL must start with 'http://' or 'https://'"
        logger.error(error_msg)
        raise WeComError(error_msg, ErrorCode.VALIDATION_ERROR)

    # Use NotifyBridge to send message via the wecom channel
    try:
        async with NotifyBridge() as nb:
            return await nb.send_async(
                "wecom",
                webhook_url=base_url,
                msg_type=msg_type,
                message=content,
                mentioned_list=mentioned_list or [],
                mentioned_mobile_list=mentioned_mobile_list or [],
            )
    except Exception as e:
        error_msg = f"Failed to send message via NotifyBridge: {e}. URL: {base_url}, Type: {msg_type}"
        logger.error(error_msg)
        raise WeComError(error_msg, ErrorCode.NETWORK_ERROR) from e


async def _process_message_response(response: Any, ctx: Context | None = None) -> dict[str, str]:
    """Process response from WeCom API.

    Args:
        response: Response from NotifyBridge
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If API call fails

    """
    # Check response
    if not getattr(response, "success", False):
        error_msg = f"Failed to send message: {response}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    # Check WeChat API response
    data = getattr(response, "data", {})
    if data.get("errcode", -1) != 0:
        error_msg = f"WeChat API error: {data.get('errmsg', 'Unknown error')}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    success_msg = "Message sent successfully"
    logger.info(success_msg)
    if ctx:
        await ctx.report_progress(1.0)
        await ctx.info(success_msg)

    return {"status": "success", "message": success_msg}


@mcp.tool(name="send_message")
async def send_message_mcp(
    content: str,
    msg_type: str = "markdown_v2",
    mentioned_list: Annotated[list[str], Field(description="List of user IDs to mention")] = [],
    mentioned_mobile_list: Annotated[list[str], Field(description="List of mobile numbers to mention")] = [],
) -> dict[str, str]:
    """Send message to WeCom.

    Args:
        content: Message content to send
        msg_type: Message type (only 'markdown_v2' is supported)
        mentioned_list: List of user IDs to mention
        mentioned_mobile_list: List of mobile numbers to mention

    Returns:
        dict: Response with status and message

    Raises:
        WeComError: If sending message fails

    """
    return await send_message(
        content=content,
        msg_type=msg_type,
        mentioned_list=mentioned_list,
        mentioned_mobile_list=mentioned_mobile_list,
        ctx=None,
    )
