"""File handling functionality for WeCom Bot MCP Server."""

# Import built-in modules
from pathlib import Path
from typing import Annotated, Any, Literal

# Import third-party modules
from loguru import logger
from mcp.server.fastmcp import Context
from notify_bridge import NotifyBridge
from pydantic import Field

# Import local modules
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.utils import get_webhook_url


async def send_wecom_file(
    file_path: str,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Send file to WeCom.

    Args:
        file_path: Path to file
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If file is not found or API call fails

    """
    if ctx:
        await ctx.report_progress(0.1)
        await ctx.info(f"Processing file: {file_path}")

    try:
        # Validate file and get webhook URL
        file_path_p = await _validate_file(file_path, ctx)
        base_url = await _get_webhook_url(ctx)

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


async def _get_webhook_url(ctx: Context | None = None) -> str:
    """Get webhook URL.

    Args:
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
        return get_webhook_url()
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
    file_path: str,
) -> dict[str, Any]:
    """Send file to WeCom.

    Args:
        file_path: Path to the file to send

    Returns:
        dict: Response with file information and status

    Raises:
        WeComError: If file sending fails

    """
    return await send_wecom_file(file_path=file_path, ctx=None)



async def upload_wecom_media(
    file_path: str,
    upload_media_type: str = "file",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Upload media to WeCom and return its media_id.

    This uses the WeCom ``upload_media`` API via notify-bridge. It does **not** send a
    message; it only uploads the file and returns the resulting ``media_id`` that can
    be reused by other WeCom APIs (for example template cards).
    """
    if ctx:
        await ctx.report_progress(0.1)
        await ctx.info(f"Uploading media: {file_path} (type={upload_media_type})")

    valid_types = ("file", "voice")
    if upload_media_type not in valid_types:
        error_msg = (
            f"Invalid upload_media_type: {upload_media_type}. "
            f"Allowed values: {', '.join(valid_types)}"
        )
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.VALIDATION_ERROR)

    try:
        file_path_p = await _validate_file(file_path, ctx)
        base_url = await _get_webhook_url(ctx)

        if ctx:
            await ctx.report_progress(0.5)
            await ctx.info("Uploading media to WeCom...")

        response = await _upload_media_to_wecom(file_path_p, base_url, upload_media_type, ctx)
        return await _process_upload_media_response(response, file_path_p, upload_media_type, ctx)
    except WeComError:
        # Already a structured WeComError, just bubble up
        raise
    except Exception as e:  # noqa: BLE001
        error_msg = f"Error uploading media: {e!s}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        # Treat generic exceptions as network-level issues for consistency with messages
        raise WeComError(error_msg, ErrorCode.NETWORK_ERROR) from e


async def _upload_media_to_wecom(
    file_path: Path,
    base_url: str,
    upload_media_type: str,
    ctx: Context | None = None,
) -> Any:
    """Upload media file to WeCom using NotifyBridge.

    Args:
        file_path: Path to the media file to upload
        base_url: Webhook URL
        upload_media_type: WeCom upload_media type ("file" or "voice")
        ctx: FastMCP context

    Returns:
        Any: Response from NotifyBridge
    """
    logger.info(f"Uploading media file: {file_path} (type={upload_media_type})")

    if ctx:
        await ctx.info(f"Uploading media: {file_path} (type={upload_media_type})")
        await ctx.report_progress(0.7)

    async with NotifyBridge() as nb:
        return await nb.send_async(
            "wecom",
            webhook_url=base_url,
            msg_type="upload_media",
            media_path=str(file_path.absolute()),
            upload_media_type=upload_media_type,
        )


async def _process_upload_media_response(
    response: Any,
    file_path: Path,
    upload_media_type: str,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Process response from WeCom upload_media API.

    Args:
        response: Response from NotifyBridge
        file_path: Path to the uploaded media file
        upload_media_type: WeCom upload_media type ("file" or "voice")
        ctx: FastMCP context

    Returns:
        dict: Response containing status, message, and media information

    Raises:
        WeComError: If API call fails or does not return a media_id
    """
    if not getattr(response, "success", False):
        error_msg = f"Failed to upload media: {response}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    data = getattr(response, "data", {}) or {}

    # Check WeCom API error code
    if data.get("errcode", 0) != 0:
        error_msg = f"WeCom upload_media API error: {data.get('errmsg', 'Unknown error')}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    media_id = data.get("media_id")
    if not media_id:
        error_msg = "WeCom upload_media API did not return media_id"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    success_msg = "Media uploaded successfully"
    logger.info(success_msg)
    if ctx:
        await ctx.report_progress(1.0)
        await ctx.info(success_msg)

    # Try to extract URL from response (for template cards and other use cases)
    media_url = None
    for key in ("url", "media_url", "file_url", "download_url"):
        value = data.get(key)
        if isinstance(value, str) and (value.startswith("http://") or value.startswith("https://")):
            media_url = value
            break

    result = {
        "status": "success",
        "message": success_msg,
        "file_name": file_path.name,
        "file_size": file_path.stat().st_size,
        "media_id": media_id,
        "media_type": data.get("type", upload_media_type),
    }

    if media_url:
        result["media_url"] = media_url

    return result


@mcp.tool(name="upload_wecom_media")
async def upload_wecom_media_mcp(
    file_path: str,
    upload_media_type: Annotated[
        Literal["file", "voice"],
        Field(
            description=(
                "WeCom upload_media type. Use 'file' for general files and 'voice' "
                "for short voice recordings."
            ),
        ),
    ] = "file",
) -> dict[str, Any]:
    """MCP tool wrapper for uploading media to WeCom.

    This tool only uploads the media and returns the resulting media_id; it does not
    send a message by itself.
    """
    return await upload_wecom_media(
        file_path=file_path,
        upload_media_type=upload_media_type,
        ctx=None,
    )
