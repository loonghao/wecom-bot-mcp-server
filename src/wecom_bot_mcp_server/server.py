"""WeCom Bot MCP Server Implementation

This module provides a server implementation for WeCom bot that follows the Model Context Protocol (MCP).
It handles message communication with WeCom webhook API and maintains message history.
"""

# Import built-in modules
import json
import os
from http import HTTPStatus
from typing import Any, Dict, List

# Import third-party modules
import httpx
from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from typing import Annotated

# Import local modules
from wecom_bot_mcp_server.logger import setup_logger

from pydantic import BaseModel, Field

# Constants
LOGGER_NAME = "wecom_bot_mcp_server"

# Initialize logger
logger = setup_logger(LOGGER_NAME)

# Load environment variables from .env file
load_dotenv()

# Create FastMCP server
mcp = FastMCP("WeCom Bot Server")

# Initialize message history
message_history: List[Dict[str, Any]] = []


class SendMessageParams(BaseModel):
    """Parameters for send_message tool."""
    content: Annotated[str, Field(
        description="The message content to send to WeCom group/chat. "
                   "Will be formatted as markdown."
    )]


@mcp.tool()
async def send_message(params: SendMessageParams) -> str:
    """Send a message to WeCom group/chat via webhook.

    This function sends a message to WeCom using the configured webhook URL.
    The message will be formatted as markdown and added to message history.

    Args:
        params: The parameters for sending the message.

    Returns:
        str: Success message if the message was sent successfully.

    Raises:
        ValueError: If content is empty/whitespace, webhook URL is not set,
                   or if there's an error sending the message.
    """
    logger.info("Received request to send message: %s", params.content)

    # Validate input
    webhook_url = os.getenv("WECOM_WEBHOOK_URL")
    if not webhook_url:
        error_msg = "WECOM_WEBHOOK_URL environment variable is not set"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if not params.content or params.content.isspace():
        error_msg = "Message content cannot be empty or whitespace"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Prepare message payload
    payload = {"msgtype": "markdown", "markdown": {"content": params.content}}
    logger.debug("Message payload prepared: %s", payload)

    # Send request
    logger.info("Sending message to WeCom")
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(webhook_url, json=payload)
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

    # Update message history
    message_history.append({"role": "assistant", "content": params.content})
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
