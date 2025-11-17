"""Image handling functionality for WeCom Bot MCP Server."""

# Import built-in modules
import os
from pathlib import Path
import tempfile
from typing import Any

# Import third-party modules
from PIL import Image
import aiohttp
from loguru import logger
from mcp.server.fastmcp import Context
from notify_bridge import NotifyBridge

# Import local modules
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.utils import get_webhook_url


async def download_image(url: str, ctx: Context | None = None) -> Path:
    """Download image from URL with retry mechanism.

    Args:
        url: URL to download image from
        ctx: FastMCP context

    Returns:
        Path: Path to downloaded image

    Raises:
        WeComError: If download fails or response is not an image

    """
    if ctx:
        await ctx.report_progress(0.2)
        await ctx.info(f"Downloading image from {url}")

    try:
        # Create a temporary file with the correct extension
        temp_dir = Path(tempfile.gettempdir()) / "wecom_images"
        os.makedirs(temp_dir, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    error_msg = f"Failed to download image: HTTP {response.status}"
                    if ctx:
                        await ctx.error(error_msg)
                    raise WeComError(
                        error_msg,
                        ErrorCode.NETWORK_ERROR,
                    )

                content_type = response.headers.get("Content-Type", "")
                if not content_type.startswith("image/"):
                    error_msg = f"Invalid content type: {content_type}"
                    if ctx:
                        await ctx.error(error_msg)
                    raise WeComError(error_msg, ErrorCode.FILE_ERROR)

                # Update file extension based on content type
                ext = content_type.split("/")[1]
                final_file = temp_dir / f"image_{hash(url)}.{ext}"

                # Write the content to the file
                with open(final_file, "wb") as f:
                    content = await response.read()
                    f.write(content)

                return final_file

    except aiohttp.ClientError as e:
        error_msg = f"Failed to download image: {e!s}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.NETWORK_ERROR) from e


async def send_wecom_image(
    image_path: str,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Send image to WeCom.

    Args:
        image_path: Path to image file or URL
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If image is not found or API call fails.

    """
    if ctx:
        await ctx.report_progress(0.1)
        await ctx.info(f"Processing image: {image_path}")

    try:
        # Process and validate image
        image_path_p = await _process_image_path(image_path, ctx)

        # Get webhook URL
        base_url = await _get_webhook_url(ctx)

        # Send image to WeCom
        if ctx:
            await ctx.report_progress(0.5)
            await ctx.info("Sending image via notify-bridge...")

        response = await _send_image_to_wecom(image_path_p, base_url)

        # Process response
        return await _process_image_response(response, image_path_p, ctx)

    except Exception as e:
        error_msg = f"Error sending image: {e!s}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.NETWORK_ERROR) from e


async def _process_image_path(image_path: str | Path, ctx: Context | None = None) -> Path:
    """Process and validate image path.

    Args:
        image_path: Path to image file or URL
        ctx: FastMCP context

    Returns:
        Path: Validated image path

    Raises:
        WeComError: If image is not found or invalid

    """
    # Handle URL
    if isinstance(image_path, str) and image_path.startswith(("http://", "https://")):
        try:
            image_path = await download_image(image_path, ctx)
        except WeComError as e:
            if ctx:
                await ctx.error(str(e))
            raise

    # Convert to Path object if string
    if isinstance(image_path, str):
        image_path = Path(image_path)

    # Check if file exists
    if not image_path.exists():
        error_msg = f"Image file not found: {image_path}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.FILE_ERROR)

    # Validate image format
    try:
        Image.open(image_path)
    except Exception as e:
        error_msg = f"Invalid image format: {e!s}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.FILE_ERROR) from e

    return image_path


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


async def _send_image_to_wecom(image_path: Path, base_url: str) -> Any:
    """Send image to WeCom using NotifyBridge.

    Args:
        image_path: Path to image
        base_url: Webhook URL

    Returns:
        Any: Response from NotifyBridge

    """
    logger.info(f"Processing image: {image_path}")

    # Use NotifyBridge to send image directly via the wecom channel
    async with NotifyBridge() as nb:
        response = await nb.send_async(
            "wecom",
            webhook_url=base_url,
            msg_type="image",
            image_path=str(image_path.absolute()),
        )

        return response


async def _process_image_response(response: Any, image_path: Path, ctx: Context | None = None) -> dict[str, Any]:
    """Process response from WeCom API.

    Args:
        response: Response from NotifyBridge
        image_path: Path to image
        ctx: FastMCP context

    Returns:
        dict: Response containing status and message

    Raises:
        WeComError: If API call fails

    """
    # Check response
    if not getattr(response, "success", False):
        error_msg = f"Failed to send image: {response}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    # Check WeChat API response
    data = getattr(response, "data", {})
    if isinstance(data, dict) and data.get("errcode", -1) != 0:
        error_msg = f"WeChat API error: {data.get('errmsg', 'Unknown error')}"
        logger.error(error_msg)
        if ctx:
            await ctx.error(error_msg)
        raise WeComError(error_msg, ErrorCode.API_FAILURE)

    success_msg = "Image sent successfully"
    logger.info(success_msg)
    if ctx:
        await ctx.report_progress(1.0)
        await ctx.info(success_msg)

    return {
        "status": "success",
        "message": success_msg,
        "image_path": str(image_path),
    }


@mcp.tool(name="send_wecom_image")
async def send_wecom_image_mcp(
    image_path: str,
) -> dict[str, Any]:
    """Send image to WeCom.

    Args:
        image_path: Path to the image file to send

    Returns:
        dict: Response with image information and status

    Raises:
        WeComError: If image sending fails

    """
    return await send_wecom_image(image_path=image_path, ctx=None)
