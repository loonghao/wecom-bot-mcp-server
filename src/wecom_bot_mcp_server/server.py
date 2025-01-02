"""WeCom Bot MCP Server Implementation

This module provides a server implementation for WeCom bot that follows the Model Context Protocol (MCP).
It handles message communication with WeCom webhook API and maintains message history.

The server provides two main functionalities:
1. Send messages to WeCom via webhook (Tool)
2. Access message history (Resource)

Example:
    To start the server:

    ```python
    if __name__ == "__main__":
        mcp.run()
    ```
"""

# Import built-in modules
import codecs
import json
import logging
import os
from http import HTTPStatus

import httpx

# Import third-party modules
from fastmcp import Context, FastMCP

# Set up logging
logger = logging.getLogger("mcp_wechat_server")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - " "%(pathname)s:%(lineno)d - %(message)s")
)
logger.addHandler(handler)

# Create FastMCP server
mcp = FastMCP("WeCom Bot Server")

# Message history storage
message_history: list[dict[str, str]] = []


def fix_encoding(text: str) -> str:
    """Fix text encoding issues"""
    try:
        # Try different encodings
        encodings = ["utf-8", "gbk", "gb2312", "gb18030"]
        for encoding in encodings:
            try:
                # First encode string to bytes, then decode
                return text.encode(encoding, errors="ignore").decode(encoding)
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue

        # If above methods fail, try using codecs
        return codecs.decode(codecs.encode(text, "utf-8", errors="ignore"), "utf-8")
    except Exception as e:
        logger.error(f"Error fixing encoding: {e!s}")
        return text


def encode_text(text: str) -> str:
    """Encode text to ensure proper handling of Chinese characters"""
    try:
        # First fix encoding issues
        fixed_text = fix_encoding(text)
        logger.debug(f"Fixed text: {fixed_text}")

        # Convert fixed text to JSON string
        return json.dumps(fixed_text, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error encoding text: {e!s}")
        return text


def decode_text(text: str) -> str:
    """Decode text from JSON format"""
    try:
        if text.startswith('"') and text.endswith('"'):
            decoded = json.loads(text)
            return fix_encoding(decoded)
        return fix_encoding(text)
    except Exception as e:
        logger.error(f"Error decoding text: {e!s}")
        return text


async def _validate_input(content: str, ctx: Context | None = None) -> None:
    """Validate input parameters for sending message.

    Args:
        content: Message content to validate
        ctx: Optional FastMCP context for logging

    Raises:
        ValueError: If content is empty/whitespace or webhook URL is not set
    """
    if not content or content.isspace():
        error_msg = "Message content cannot be empty or whitespace"
        if ctx:
            ctx.error(error_msg)
        raise ValueError(error_msg)

    webhook_url = os.getenv("WECOM_WEBHOOK_URL")
    if not webhook_url:
        error_msg = "WECOM_WEBHOOK_URL environment variable is not set"
        if ctx:
            ctx.error(error_msg)
        raise ValueError(error_msg)


async def _prepare_message(content: str) -> dict:
    """Prepare message payload for WeChat API.

    Args:
        content: Message content to prepare

    Returns:
        dict: Prepared message payload
    """
    # Encode content to handle Chinese characters
    encoded_content = encode_text(content)

    # Create message payload
    return {"msgtype": "markdown", "markdown": {"content": encoded_content}}


async def _send_http_request(url: str, payload: dict, ctx: Context | None = None) -> dict:
    """Send HTTP request to WeChat API.

    Args:
        url: Webhook URL
        payload: Message payload
        ctx: Optional FastMCP context for logging

    Returns:
        dict: API response data

    Raises:
        ValueError: If request fails or response is invalid
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response content: {response.text}")

            if response.status_code != HTTPStatus.OK:
                error_msg = f"Failed to send message: {response.text}"
                if ctx:
                    ctx.error(error_msg)
                message_history.append({"role": "assistant", "error": error_msg})
                raise ValueError(error_msg) from None

            return response.json()

        except httpx.TimeoutException as e:
            error_msg = f"Request timeout: {e!s}"
            if ctx:
                ctx.error(error_msg)
            message_history.append({"role": "assistant", "error": error_msg})
            raise ValueError(error_msg) from e

        except httpx.RequestError as e:
            error_msg = f"HTTP request failed: {e!s}"
            if ctx:
                ctx.error(error_msg)
            message_history.append({"role": "assistant", "error": error_msg})
            raise ValueError(error_msg) from e


@mcp.tool()
async def send_message(content: str, ctx: Context | None = None) -> str:
    """Send a message to WeCom group/chat via webhook.

    This function sends a message to WeCom using the configured webhook URL.
    The message will be formatted as markdown and added to message history.

    Args:
        content: The message content to send. Cannot be empty or whitespace.
        ctx: Optional FastMCP context for logging and progress tracking.

    Returns:
        str: Success message if the message was sent successfully.

    Raises:
        ValueError: If content is empty/whitespace, webhook URL is not set,
                   or if there's an error sending the message.
    """
    try:
        # Input validation
        await _validate_input(content, ctx)
        webhook_url = os.getenv("WECOM_WEBHOOK_URL")

        # Progress tracking
        if ctx:
            ctx.info("Preparing to send message...")

        # Prepare message
        payload = await _prepare_message(content)

        # Send request
        if ctx:
            ctx.info("Sending message...")
        response_data = await _send_http_request(webhook_url, payload, ctx)

        # Check WeChat API response
        if response_data.get("errcode") != 0:
            error_msg = f"WeChat API error: {response_data.get('errmsg', 'Unknown error')}"
            if ctx:
                ctx.error(error_msg)
            message_history.append({"role": "assistant", "error": error_msg})
            raise ValueError(error_msg) from None

        # Success - add to history
        message_history.append({"role": "assistant", "content": content})

        success_msg = "Message sent successfully"
        if ctx:
            ctx.info(success_msg)
        return success_msg

    except Exception as e:
        error_msg = f"Unexpected error: {e!s}"
        if ctx:
            ctx.error(error_msg)
        message_history.append({"role": "assistant", "error": error_msg})
        raise ValueError(error_msg) from e


@mcp.resource("config://message-history")
def get_message_history() -> str:
    """Get message history as a formatted string.

    This function returns the message history as a newline-separated string,
    where each line contains the role and content of a message.

    Returns:
        str: Formatted message history string. Empty string if no messages.
    """
    return "\n".join(
        f"{msg.get('role', 'unknown')}: {msg.get('content', '')} ({msg.get('status', 'unknown')})"
        for msg in message_history
    )


def main() -> None:
    """Entry point for the WeCom Bot MCP Server.

    This function starts the FastMCP server for handling WeCom bot messages.
    """
    mcp.run()


if __name__ == "__main__":
    main()
