"""File handling functionality for WeCom Bot MCP Server."""

# Import built-in modules
from pathlib import Path
from typing import Annotated
from typing import Any

# Import third-party modules
from loguru import logger
from mcp.server.fastmcp import Context
from notify_bridge import NotifyBridge
from pydantic import Field

# Import local modules
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.bot_config import get_bot_registry
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError


async def send_wecom_file(
    file_path: str,
    bot_id: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Send file to WeCom.

    Args:
        file_path: Path to file
        bot_id: Bot identifier for multi-bot setups. If None, uses the default bot.
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If file is not found or API call fails

    """
    if ctx:
        await ctx.report_progress(0.1)
        await ctx.info(f"Processing file: {file_path}" + (f" via bot '{bot_id}'" if bot_id else ""))

    try:
        # Validate file and get webhook URL
        file_path_p = await _validate_file(file_path, ctx)
        base_url = await _get_webhook_url(bot_id, ctx)

        # Send file to WeCom
        if ctx:
            await ctx.report_progress(0.5)
            await ctx.info("Sending file to WeCom...")

        response = await _send_file_to_wecom(file_path_p, base_url, ctx)

        # Process response
        return await _process_file_response(response, file_path_p, ctx)

    except Exception as e:
        error_msg = f"Error sending file: {e!s}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.UNKNOWN) from e


async def _validate_file(file_path: str | Path, ctx: Context | None = None) -> Path:
    """Validate file existence and type.

    Args:
        file_path: Path to file
        ctx: FastMCP context

    Returns:
        Path: Validated file path

    Raises:
        WeComError: If file is not found or not a file

    """
    if ctx:
        await ctx.report_progress(0.2)
        await ctx.info(f"Validating file: {file_path}")

    # Convert to Path object if string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Validate file
    if not file_path.exists():
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.FILE_ERROR)

    if not file_path.is_file():
        error_msg = f"Not a file: {file_path}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.FILE_ERROR)

    return file_path


async def _get_webhook_url(bot_id: str | None = None, ctx: Context | None = None) -> str:
    """Get webhook URL for a specific bot.

    Args:
        bot_id: Bot identifier. If None, uses the default bot.
        ctx: FastMCP context

    Returns:
        str: Webhook URL

    Raises:
        WeComError: If webhook URL is not found

    """
    if ctx:
        await ctx.report_progress(0.3)
        await ctx.info("Getting webhook URL")

    try:
        return get_bot_registry().get_webhook_url(bot_id)
    except WeComError as e:
        if ctx:
            await ctx.error(str(e))
        raise


async def _send_file_to_wecom(file_path: Path, base_url: str, ctx: Context | None = None) -> Any:
    """Send file to WeCom using NotifyBridge.

    Args:
        file_path: Path to file
        base_url: Webhook URL
        ctx: FastMCP context

    Returns:
        Any: Response from NotifyBridge

    """
    logger.info(f"Processing file: {file_path}")

    if ctx:
        await ctx.info(f"Sending file: {file_path}")
        await ctx.report_progress(0.7)

    # Use NotifyBridge to send file directly via the wecom channel
    # NOTE:
    #   The notify-bridge WeCom notifier expects the file path in the
    #   ``media_path`` field when sending a ``msg_type="file"`` message.
    #   Using any other field name (like ``file_path``) will cause
    #   notify-bridge to raise "Either media_id or media_path is required
    #   for file message" and the upload will fail.
    async with NotifyBridge() as nb:
        return await nb.send_async(
            "wecom",
            webhook_url=base_url,
            msg_type="file",
            media_path=str(file_path.absolute()),
        )


async def _process_file_response(response: Any, file_path: Path, ctx: Context | None = None) -> dict[str, Any]:
    """Process response from WeCom API.

    Args:
        response: Response from NotifyBridge
        file_path: Path to file
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If API call fails

    """
    # Check response
    if not getattr(response, "success", False):
        error_msg = f"Failed to send file: {response}"
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

    success_msg = "File sent successfully"
    logger.info(success_msg)
    if ctx:
        await ctx.report_progress(1.0)
        await ctx.info(success_msg)

    return {
        "status": "success",
        "message": success_msg,
        "file_name": file_path.name,
        "file_size": file_path.stat().st_size,
        "media_id": data.get("media_id", ""),
    }


@mcp.tool(name="send_wecom_file")
async def send_wecom_file_mcp(
    file_path: Annotated[str, Field(description="Path to the file to send")],
    bot_id: Annotated[
        str | None,
        Field(
            description=(
                "Bot identifier for multi-bot setups. If not specified, uses the default bot. "
                "Use `list_wecom_bots` tool to see available bots."
            )
        ),
    ] = None,
) -> dict[str, Any]:
    """Send file to WeCom.

    Args:
        file_path: Path to the file to send
        bot_id: Bot identifier for multi-bot setups. If None, uses the default bot.

    Returns:
        dict: Response with file information and status

    Raises:
        WeComError: If file sending fails

    """
    return await send_wecom_file(file_path=file_path, bot_id=bot_id, ctx=None)
