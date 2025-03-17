"""Message handling functionality for WeCom Bot MCP Server."""

# Import built-in modules
from typing import Any

# Import third-party modules
from loguru import logger
from mcp.server.fastmcp import Context
from notify_bridge import NotifyBridge

# Import local modules
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.utils import encode_text
from wecom_bot_mcp_server.utils import get_webhook_url

# Constants
MESSAGE_HISTORY_KEY = "history://messages"

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


@mcp.tool()
async def send_message(
    content: str,
    msg_type: str = "markdown",
    mentioned_list: list[str] | None = None,
    mentioned_mobile_list: list[str] | None = None,
    ctx: Context | None = None,
) -> dict[str, str]:
    """Send message to WeCom.

    Args:
        content: Message content
        msg_type: Message type (text, markdown)
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

    # Validate message type
    if msg_type not in ["text", "markdown"]:
        error_msg = f"Invalid message type: {msg_type}"
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


async def _prepare_message_content(content: str, ctx: Context | None = None, msg_type: str = "text") -> str:
    """Prepare message content for sending.

    Args:
        content: Message content
        ctx: FastMCP context
        msg_type: Message type (text, markdown, etc.)

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

    # Use NotifyBridge to send message
    try:
        async with NotifyBridge() as nb:
            return await nb.send_async(
                "wecom",
                {
                    "base_url": base_url,
                    "msg_type": msg_type,
                    "content": content,
                    "mentioned_list": mentioned_list or [],
                    "mentioned_mobile_list": mentioned_mobile_list or [],
                },
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
