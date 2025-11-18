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
        "- Images embedded with ![alt](url), e.g. ![chart](https://example.com/chart.png)\n"
        "- Horizontal rules (---)\n\n"
        "## Image sending recommendations\n"
        "- If the main content is a standalone image file or screenshot, "
        "send it with the send_wecom_image tool (msg_type=image), passing the local file path as `image_path`.\n"
        "- If the image is just an illustration inside a larger report, "
        "use markdown_v2 and embed it with ![alt](url).\n\n"
        "## File sending recommendations\n"
        "- Use the send_wecom_file tool when sending non-image files such as "
        "reports, logs, or archives.\n"
        "- Local file paths are acceptable for `file_path`; this server will upload the file to WeCom "
        "via NotifyBridge and recipients will see it as an attached file message.\n"
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
        "- When you have an image URL that should appear inside the text, embed it inline "
        "using markdown_v2 image syntax: ![description](image_url).\n"
        "- You may reference local filesystem images (e.g. C:\\path\\to\\image.png or /tmp/image.png); "
        "this server will attempt to upload them via the WeCom file API and rewrite the markdown to use a "
        "remote URL when possible. If upload fails, the original path is kept as a fallback.\n"
        "- Do not request `text` or legacy `markdown` msg_type; they will be rejected as invalid.\n"
        "- If the main content is an image file (local path or URL), "
        "call the `send_wecom_image` tool instead of embedding it in markdown.\n"
        "- If the user asks to send a non-image file (reports, logs, archives), "
        "call the `send_wecom_file` tool with the local file path.\n"
        "- It is safe to pass local file/image paths to these tools; this server will call NotifyBridge "
        "to upload the file to WeCom so recipients can access it.\n"
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

        fixed_content = await _prepare_message_content(content, msg_type, ctx)

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


async def _prepare_message_content(content: str, msg_type: str = "markdown_v2", ctx: Context | None = None) -> str:
    """Prepare message content for sending.

    Args:
        content: Message content
        msg_type: Message type (only 'markdown_v2' is supported)
        ctx: FastMCP context

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


async def send_wecom_template_card(
    template_card_type: str,
    *,
    template_card_source: dict[str, Any] | None = None,
    template_card_main_title: dict[str, Any] | None = None,
    template_card_emphasis_content: dict[str, Any] | None = None,
    template_card_quote_area: dict[str, Any] | None = None,
    template_card_sub_title_text: str | None = None,
    template_card_horizontal_content_list: list[dict[str, Any]] | None = None,
    template_card_vertical_content_list: list[dict[str, Any]] | None = None,
    template_card_jump_list: list[dict[str, Any]] | None = None,
    template_card_card_action: dict[str, Any] | None = None,
    template_card_image: dict[str, Any] | None = None,
    template_card_image_text_area: dict[str, Any] | None = None,
    ctx: Context | None = None,
) -> dict[str, str]:
    """Send a WeCom template card message.

    This wraps notify-bridge ``msg_type="template_card"`` with the supported
    ``template_card_type`` values ``text_notice`` and ``news_notice``.

    Note:
        All image URLs in template cards (icon_url, image_url, etc.) must be
        HTTP(S) URLs. Local file paths are not supported. If you have a local
        image, please upload it to a public server or CDN first.

    """
    if ctx:
        await ctx.report_progress(0.1)
        await ctx.info(f"Sending template_card ({template_card_type}) message")

    valid_types = ("text_notice", "news_notice")
    if template_card_type not in valid_types:
        error_msg = f"Invalid template_card_type: {template_card_type}. Allowed values: {', '.join(valid_types)}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.VALIDATION_ERROR)

    required_fields = {
        "template_card_source": template_card_source,
        "template_card_main_title": template_card_main_title,
        "template_card_card_action": template_card_card_action,
    }
    missing = [name for name, value in required_fields.items() if value is None]
    if missing:
        error_msg = f"Missing required template card fields: {', '.join(missing)}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.VALIDATION_ERROR)

    try:
        base_url = await _get_webhook_url(ctx)

        if ctx:
            await ctx.report_progress(0.3)
            await ctx.info("Sending template card via notify-bridge...")

        template_kwargs: dict[str, Any] = {
            "template_card_source": template_card_source,
            "template_card_main_title": template_card_main_title,
            "template_card_card_action": template_card_card_action,
        }
        if template_card_emphasis_content is not None:
            template_kwargs["template_card_emphasis_content"] = template_card_emphasis_content
        if template_card_quote_area is not None:
            template_kwargs["template_card_quote_area"] = template_card_quote_area
        if template_card_sub_title_text is not None:
            template_kwargs["template_card_sub_title_text"] = template_card_sub_title_text
        if template_card_horizontal_content_list:
            template_kwargs["template_card_horizontal_content_list"] = template_card_horizontal_content_list
        if template_card_vertical_content_list:
            template_kwargs["template_card_vertical_content_list"] = template_card_vertical_content_list
        if template_card_jump_list:
            template_kwargs["template_card_jump_list"] = template_card_jump_list
        if template_card_image is not None:
            template_kwargs["template_card_image"] = template_card_image
        if template_card_image_text_area is not None:
            template_kwargs["template_card_image_text_area"] = template_card_image_text_area

        response = await _send_template_card_to_wecom(
            base_url=base_url,
            template_card_type=template_card_type,
            **template_kwargs,
        )
        return await _process_template_card_response(response, ctx)
    except Exception as e:
        error_msg = f"Error sending template card: {e!s}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.NETWORK_ERROR) from e


async def _send_template_card_to_wecom(
    base_url: str,
    template_card_type: str,
    **template_kwargs: Any,
) -> Any:
    """Send a template card message to WeCom using NotifyBridge.

    Args:
        base_url: Webhook URL
        template_card_type: Template card type ("text_notice" or "news_notice")
        template_kwargs: Template card-specific keyword arguments

    Returns:
        Any: Response from NotifyBridge

    """
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        error_msg = f"Invalid webhook URL format: '{base_url}'. URL must start with 'http://' or 'https://'"
        logger.error(error_msg)
        raise WeComError(error_msg, ErrorCode.VALIDATION_ERROR)

    try:
        # Debug: log the template_kwargs
        logger.debug(f"Sending template card with kwargs: {template_kwargs}")

        async with NotifyBridge() as nb:
            return await nb.send_async(
                "wecom",
                webhook_url=base_url,
                msg_type="template_card",
                template_card_type=template_card_type,
                **template_kwargs,
            )
    except Exception as e:
        error_msg = (
            f"Failed to send template card via NotifyBridge: {e}. URL: {base_url}, "
            f"template_card_type: {template_card_type}"
        )
        logger.error(error_msg)
        raise WeComError(error_msg, ErrorCode.NETWORK_ERROR) from e


async def _process_template_card_response(
    response: Any,
    ctx: Context | None = None,
) -> dict[str, str]:
    """Process response from WeCom template_card API.

    Args:
        response: Response from NotifyBridge
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If API call fails

    """
    if not getattr(response, "success", False):
        error_msg = f"Failed to send template card: {response}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    data = getattr(response, "data", {}) or {}
    if data.get("errcode", -1) != 0:
        error_msg = f"WeChat API error: {data.get('errmsg', 'Unknown error')}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    success_msg = "Template card sent successfully"
    logger.info(success_msg)
    if ctx:
        await ctx.report_progress(1.0)
        await ctx.info(success_msg)

    return {"status": "success", "message": success_msg}


@mcp.tool(name="send_wecom_template_card_text_notice")
async def send_wecom_template_card_text_notice_mcp(
    template_card_source: Annotated[
        dict[str, Any],
        Field(description="Source info for the card (icon_url, desc, desc_color, etc.)"),
    ],
    template_card_main_title: Annotated[
        dict[str, Any],
        Field(description="Main title and description for the card."),
    ],
    template_card_card_action: Annotated[
        dict[str, Any],
        Field(description="Primary click action for the card."),
    ],
    template_card_emphasis_content: Annotated[
        dict[str, Any] | None,
        Field(description="Emphasised numeric content area."),
    ] = None,
    template_card_quote_area: Annotated[
        dict[str, Any] | None,
        Field(description="Quote area configuration."),
    ] = None,
    template_card_sub_title_text: Annotated[
        str | None,
        Field(description="Subtitle text under the main title."),
    ] = None,
    template_card_horizontal_content_list: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Horizontal content items."),
    ] = None,
    template_card_jump_list: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Jump (link) buttons."),
    ] = None,
    ctx: Context | None = None,
) -> dict[str, str]:
    """MCP tool wrapper for sending a text_notice template card.

    The structure of the template card fields follows the WeCom template_card
    documentation and notify-bridge examples.
    """
    return await send_wecom_template_card(
        template_card_type="text_notice",
        template_card_source=template_card_source,
        template_card_main_title=template_card_main_title,
        template_card_emphasis_content=template_card_emphasis_content,
        template_card_quote_area=template_card_quote_area,
        template_card_sub_title_text=template_card_sub_title_text,
        template_card_horizontal_content_list=template_card_horizontal_content_list,
        template_card_vertical_content_list=None,
        template_card_jump_list=template_card_jump_list,
        template_card_card_action=template_card_card_action,
        template_card_image=None,
        template_card_image_text_area=None,
        ctx=ctx,
    )


@mcp.tool(name="send_wecom_template_card_news_notice")
async def send_wecom_template_card_news_notice_mcp(
    template_card_source: Annotated[
        dict[str, Any],
        Field(description="Source info for the card (icon_url, desc, desc_color, etc.)"),
    ],
    template_card_main_title: Annotated[
        dict[str, Any],
        Field(description="Main title and description for the card."),
    ],
    template_card_card_action: Annotated[
        dict[str, Any],
        Field(description="Primary click action for the card."),
    ],
    template_card_image: Annotated[
        dict[str, Any] | None,
        Field(
            description="Main image configuration for the news_notice card. "
            "Should contain 'url' and optionally 'aspect_ratio'."
        ),
    ] = None,
    template_card_image_text_area: Annotated[
        dict[str, Any] | None,
        Field(description="Image text area configuration. Should contain 'image_url', 'title', 'desc', etc."),
    ] = None,
    template_card_quote_area: Annotated[
        dict[str, Any] | None,
        Field(description="Quote area configuration."),
    ] = None,
    template_card_vertical_content_list: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Vertical content items."),
    ] = None,
    template_card_horizontal_content_list: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Horizontal content items."),
    ] = None,
    template_card_jump_list: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Jump (link) buttons."),
    ] = None,
    ctx: Context | None = None,
) -> dict[str, str]:
    """MCP tool wrapper for sending a news_notice template card."""
    return await send_wecom_template_card(
        template_card_type="news_notice",
        template_card_source=template_card_source,
        template_card_main_title=template_card_main_title,
        template_card_emphasis_content=None,
        template_card_quote_area=template_card_quote_area,
        template_card_sub_title_text=None,
        template_card_horizontal_content_list=template_card_horizontal_content_list,
        template_card_vertical_content_list=template_card_vertical_content_list,
        template_card_jump_list=template_card_jump_list,
        template_card_card_action=template_card_card_action,
        template_card_image=template_card_image,
        template_card_image_text_area=template_card_image_text_area,
        ctx=ctx,
    )
