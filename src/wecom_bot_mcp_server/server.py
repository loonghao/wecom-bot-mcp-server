"""WeCom Bot MCP Server Implementation

This module provides a server implementation for WeCom bot that follows the Model Context Protocol (MCP).
It handles message communication with WeCom webhook API and maintains message history.
"""

# Import built-in modules
import asyncio
from http import HTTPStatus
import json
import logging
import os
from typing import Annotated, Any, Dict, List

# Import third-party modules
from dotenv import load_dotenv
from fastmcp import Context, FastMCP
import httpx
from pydantic import BaseModel, Field
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

# Import local modules
from wecom_bot_mcp_server.logger import setup_logger
from wecom_bot_mcp_server.text_utils import encode_text

# Constants
LOGGER_NAME = "wecom_bot_mcp_server"
MAX_RETRIES = 3
INITIAL_WAIT_SECONDS = 1
MAX_WAIT_SECONDS = 10
REQUEST_TIMEOUT = 60.0  # 60 seconds timeout

# Setup logger
logger = setup_logger(LOGGER_NAME)

# Load environment variables
load_dotenv()

# Initialize FastMCP
mcp = FastMCP("WeCom Bot Server")

# Store message history
message_history: List[Dict[str, Any]] = []


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=INITIAL_WAIT_SECONDS, max=MAX_WAIT_SECONDS),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPError)),
    before_sleep=lambda retry_state: logger.warning(
        "Retry attempt %d after error: %s",
        retry_state.attempt_number,
        retry_state.outcome.exception()
    )
)
async def _send_request(url: str, payload: dict) -> dict:
    """Send HTTP request with retry logic.

    Args:
        url: The webhook URL to send request to
        payload: The request payload

    Returns:
        dict: Response data from the API

    Raises:
        ValueError: If the request fails after all retries
    """
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.post(url, json=payload)
        logger.debug("Response status: %d, content: %s", response.status_code, response.text)

        if response.status_code != HTTPStatus.OK:
            error_msg = f"HTTP error {response.status_code}: {response.text}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        response_data = response.json()
        if response_data.get("errcode") != 0:
            error_msg = f"WeChat API error {response_data.get('errcode')}: {response_data.get('errmsg', 'Unknown error')}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        return response_data


@mcp.tool(description="Send a message to WeCom group/chat via webhook.")
async def send_message(content: Annotated[str, Field(
        description="The message content to send to WeCom group/chat. "
                   "Will be formatted as markdown."
    )]
) -> str:
    """Send a message to WeCom group/chat via webhook.

    This function sends a message to WeCom using the configured webhook URL.
    The message will be formatted as markdown and added to message history.

    Args:
        content: The message content to send to WeCom group/chat.

    Returns:
        str: Success message if the message was sent successfully.

    Raises:
        ValueError: If content is empty/whitespace, webhook URL is not set,
                   or if there's an error sending the message.
    """
    # Validate input
    webhook_url = os.getenv("WECOM_WEBHOOK_URL")
    if not webhook_url:
        error_msg = "WECOM_WEBHOOK_URL environment variable is not set"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Encode content to handle Chinese characters
    try:
        encoded_content = encode_text(content)
    except Exception as e:
        error_msg = f"Failed to encode message: {e}"
        logger.error(error_msg)
        return "xxxxx"

    logger.debug("Encoded content: %s", encoded_content)

    # Prepare message payload
    payload = {"msgtype": "markdown", "markdown": {"content": encoded_content}}
    logger.debug("Message payload prepared: %s", payload)

    # Send request with retry logic
    try:
        await _send_request(webhook_url, payload)
    except Exception as e:
        error_msg = f"Failed to send message after {MAX_RETRIES} retries: {e}"
        logger.error(error_msg)
        return error_msg

    # Update message history
    message_history.append({"role": "assistant", "content": encoded_content})
    logger.debug("Message history updated, length: %d", len(message_history))

    success_msg = "Message sent successfully"
    logger.info(success_msg)
    return success_msg


@mcp.resource("resource://message-history")
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
    try:
        mcp.run()
    except Exception as e:
        logger.error("Failed to start server: %s", e, exc_info=True)
        raise

if __name__ == "__main__":
    main()
