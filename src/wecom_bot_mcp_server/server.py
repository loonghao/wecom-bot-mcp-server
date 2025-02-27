"""WeCom Bot MCP Server.

This module provides a FastMCP server for interacting with WeCom (WeChat Work) bot.
It supports sending messages and files through WeCom's webhook API.
"""

# Import built-in modules
import logging
import os
from pathlib import Path
import sys
import tempfile

# Import third-party modules
from PIL import Image
from fastmcp import Context
from fastmcp import FastMCP
import ftfy
import httpx
from notify_bridge import NotifyBridge
from platformdirs import user_log_dir
from pydantic import BaseModel
from pydantic import Field

# Import local modules
from wecom_bot_mcp_server import __version__

# Type aliases
ResponseDict = dict[str, str | dict]

# Constants
APP_NAME = "wecom-bot-mcp-server"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = os.getenv("MCP_LOG_LEVEL", "DEBUG").upper()
LOG_DIR = Path(user_log_dir(APP_NAME, appauthor="hal"))
LOG_FILE = os.getenv("MCP_LOG_FILE", str(LOG_DIR / "mcp_wecom.log"))

# Message history storage
message_history: list[dict[str, str]] = []


def get_message_history() -> str:
    """Get formatted message history.

    Returns:
        str: Formatted message history string

    """
    if not message_history:
        return ""
    return "\n".join(msg["content"] for msg in message_history)


class MessageContent(BaseModel):
    """Message content model for WeCom notifications."""

    content: str = Field(..., description="Message content")
    mentioned_list: list[str] | None = Field(None, description="List of user IDs to mention")
    mentioned_mobile_list: list[str] | None = Field(None, description="List of mobile numbers to mention")


class MessageResponse(BaseModel):
    """Response model for WeCom operations."""

    status: str = Field(..., description="Status of the operation (success/error)")
    message: str = Field(..., description="Response message")
    details: dict | None = Field(None, description="Additional details or error information")

    @classmethod
    def success(cls, message: str, details: dict | None = None) -> ResponseDict:
        """Create a success response."""
        return cls(status="success", message=message, details=details).dict()

    @classmethod
    def error(cls, message: str, error_type: str, details: dict | None = None) -> ResponseDict:
        """Create an error response."""
        error_details = {"error_type": error_type, **(details or {})}
        return cls(status="error", message=message, details=error_details).dict()


def setup_logging() -> logging.Logger:
    """Configure logging settings for the application.

    Returns:
        logging.Logger: Configured logger instance

    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("mcp_wechat_server")
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Configure handlers with common formatter
    formatter = logging.Formatter(LOG_FORMAT)

    # Add file handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(f"Log file location: {LOG_FILE}")
    return logger


# Initialize FastMCP server and logger
LOGGER = setup_logging()
mcp = FastMCP(
    name=APP_NAME,
    version=__version__,
    description="WeCom Bot MCP Server - A Python server for WeCom bot following the Model Context Protocol",
)


def get_webhook_url() -> str:
    """Get WeCom webhook URL from environment variables.

    Returns:
        str: Webhook URL

    Raises:
        KeyError: If WECOM_WEBHOOK_URL is not set

    """
    return os.environ["WECOM_WEBHOOK_URL"]


def encode_text(text: str) -> str:
    """Encode text for sending to WeCom.

    Uses ftfy to automatically fix text encoding issues and normalize Unicode.
    Then returns the text wrapped in double quotes with proper escaping.

    Args:
        text: Input text that may have encoding issues

    Returns:
        str: Fixed text with proper handling of Unicode characters, wrapped in double quotes.

    Raises:
        ValueError: If text encoding fails

    """
    try:
        # Fix text encoding and normalize Unicode
        fixed_text = ftfy.fix_text(text)
        # Escape special characters and wrap in double quotes
        escaped_text = fixed_text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
        return f'"{escaped_text}"'
    except Exception as e:
        LOGGER.error(f"Error encoding text: {e!s}")
        raise ValueError(f"Failed to encode text: {e!s}") from e


@mcp.tool("send_wecom_message")
async def send_message(
    content: str,
    msg_type: str = "markdown",
    mentioned_list: list[str] | None = None,
    mentioned_mobile_list: list[str] | None = None,
    ctx: Context | None = None,
) -> str:
    """Send message to WeCom.

    Args:
        content: Message content
        msg_type: Message type (text, markdown)
        mentioned_list: List of mentioned users
        mentioned_mobile_list: List of mentioned mobile numbers
        ctx: FastMCP context

    Returns:
        str: Success message if message is sent successfully

    Raises:
        ValueError: If message content is empty or API call fails

    """
    try:
        if not content:
            raise ValueError("Message content cannot be empty")

        try:
            base_url = get_webhook_url()
        except KeyError as e:
            raise ValueError("WECOM_WEBHOOK_URL environment variable is not set") from e

        # Add message to history
        message_history.append({"role": "assistant", "content": content})

        # Fix text encoding and convert to JSON string
        fixed_content = encode_text(content)

        LOGGER.info(f"Sending message: {fixed_content}")
        if ctx:
            ctx.progress("Sending message...")

        async with NotifyBridge() as nb:
            response = await nb.send_async(
                "wecom",
                {
                    "base_url": base_url,
                    "msg_type": msg_type,
                    "content": fixed_content,
                    "mentioned_list": mentioned_list or [],
                    "mentioned_mobile_list": mentioned_mobile_list or [],
                },
            )

        if hasattr(response, "is_success") and response.is_success:
            return "Message sent successfully"
        else:
            return f"Failed to send message: {response}"

    except Exception as e:
        LOGGER.error(f"Error sending message: {e!s}")
        raise ValueError(f"Failed to send message: {e!s}") from e


@mcp.tool("send_wecom_file")
async def send_wecom_file(file_path: str, ctx: Context | None = None) -> str:
    """Send file to WeCom.

    Args:
        file_path: Path to file
        ctx: FastMCP context

    Returns:
        str: Success message if file is sent successfully

    Raises:
        ValueError: If file is not found or API call fails

    """
    try:
        if not os.path.exists(file_path):
            raise ValueError("File not found")

        try:
            base_url = get_webhook_url()
        except KeyError as e:
            raise ValueError("WECOM_WEBHOOK_URL environment variable is not set") from e

        LOGGER.info(f"Preparing to send file: {file_path}")
        if ctx:
            ctx.progress("Sending file...")

        async with NotifyBridge() as nb:
            response = await nb.send_async(
                "wecom",
                {
                    "base_url": base_url,
                    "msg_type": "file",
                    "file_path": file_path,
                },
            )

        if response.status_code != 200:
            raise ValueError(f"Failed to send file: HTTP {response.status_code}")

        if ctx:
            ctx.progress("File sent successfully")

        return "File sent successfully"

    except Exception as e:
        LOGGER.error(f"Error sending file: {e!s}")
        raise ValueError(f"Failed to send file: {e!s}") from e


async def _download_image(url: str) -> str:
    """Download image from URL.

    Args:
        url: Image URL

    Returns:
        str: Path to downloaded image

    Raises:
        ValueError: If download fails

    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise ValueError(f"Failed to download image: {e!s}") from e

        # Create a temporary file to save the downloaded image
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name


def _convert_svg_to_png(svg_path: str) -> str:
    """Convert SVG to PNG.

    Args:
        svg_path: Path to SVG file

    Returns:
        str: Path to converted PNG file

    Raises:
        ValueError: If conversion fails

    """
    try:
        # Import third-party modules
        from reportlab.graphics import renderPM
        from svglib.svglib import svg2rlg

        # Convert SVG to PNG
        temp_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, temp_png.name, fmt="PNG")
        temp_png.close()
        return temp_png.name
    except ImportError as e:
        raise ValueError("SVG support requires svglib package") from e
    except Exception as e:
        raise ValueError(f"Failed to convert SVG: {e!s}") from e


def _validate_image(image_path: str) -> None:
    """Validate image format.

    Args:
        image_path: Path to image file

    Raises:
        ValueError: If image format is invalid

    """
    try:
        with Image.open(image_path) as img:
            if img.format.lower() not in ["png", "jpg", "jpeg", "gif"]:
                raise ValueError("Invalid image format")
    except Exception as e:
        raise ValueError(f"Failed to open image: {e!s}") from e


@mcp.tool("send_wecom_image")
async def send_wecom_image(image_path: str, ctx: Context | None = None) -> str:
    """Send image to WeCom.

    Args:
        image_path: Path to image file or URL
        ctx: FastMCP context

    Returns:
        str: Success message if image is sent successfully

    Raises:
        ValueError: If image is not found or API call fails

    """
    try:
        # Handle URL case
        if image_path.startswith(("http://", "https://")):
            image_path = await _download_image(image_path)

        # Check if file exists
        if not os.path.exists(image_path):
            raise ValueError("Image not found")

        # Handle SVG files
        if image_path.lower().endswith(".svg"):
            image_path = _convert_svg_to_png(image_path)

        # Validate image format
        _validate_image(image_path)

        try:
            base_url = get_webhook_url()
        except KeyError as e:
            raise ValueError("WECOM_WEBHOOK_URL environment variable is not set") from e

        LOGGER.info(f"Preparing to send image: {image_path}")
        if ctx:
            ctx.progress("Sending image...")

        async with NotifyBridge() as nb:
            response = await nb.send_async(
                "wecom",
                {
                    "base_url": base_url,
                    "msg_type": "image",
                    "image_path": image_path,
                },
            )

        if response.status_code != 200:
            raise ValueError(f"Failed to send image: HTTP {response.status_code}")

        if ctx:
            ctx.progress("Image sent successfully")

        return "Image sent successfully"

    except Exception as e:
        LOGGER.error(f"Error sending image: {e!s}")
        raise ValueError(f"Failed to send image: {e!s}") from e


def main() -> None:
    """Start the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
