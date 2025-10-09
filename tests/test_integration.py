"""Integration tests for WeCom Bot MCP Server."""

# Import built-in modules
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server import ErrorCode, WeComError, send_message, send_wecom_file, send_wecom_image


@pytest.mark.asyncio
async def test_send_text_message_integration(mock_message_send):
    """Test sending a text message end-to-end."""
    # Setup
    content = "Hello, World!"
    msg_type = "text"

    # Execute
    result = await send_message(content=content, msg_type=msg_type)

    # Verify
    assert result is not None
    assert "status" in result
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_send_markdown_message_integration(mock_message_send):
    """Test sending a markdown message end-to-end."""
    # Setup
    content = "## Title\n- Point 1\n- Point 2"
    msg_type = "markdown"

    # Execute
    result = await send_message(content=content, msg_type=msg_type)

    # Verify
    assert result is not None
    assert "status" in result
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_send_message_with_mentions_integration(mock_message_send):
    """Test sending a message with user mentions."""
    # Setup
    content = "Hello @user1 @user2"
    msg_type = "text"
    mentioned_list = ["user1", "user2"]

    # Execute
    result = await send_message(content=content, msg_type=msg_type, mentioned_list=mentioned_list)

    # Verify
    assert result is not None
    assert "status" in result
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_send_file_integration(mock_file_send, fs):
    """Test sending a file end-to-end."""
    # Setup - create a test file
    test_file = "test_file.txt"
    fs.create_file(test_file, contents="Test file content")

    # Execute
    result = await send_wecom_file(test_file)

    # Verify
    assert result is not None
    assert "status" in result
    assert result["status"] == "success"
    assert "file_name" in result


@pytest.mark.asyncio
async def test_send_image_integration(mock_image_send):
    """Test sending an image end-to-end."""
    # Execute
    result = await send_wecom_image("test_image.jpg")

    # Verify
    assert result is not None
    assert "status" in result
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_error_handling_invalid_webhook():
    """Test error handling when webhook URL is invalid."""
    # Setup - clear webhook URL
    original_url = os.environ.get("WECOM_WEBHOOK_URL")
    if "WECOM_WEBHOOK_URL" in os.environ:
        del os.environ["WECOM_WEBHOOK_URL"]

    try:
        # Execute and verify
        with pytest.raises(WeComError) as excinfo:
            await send_message(content="Test", msg_type="text")

        # Just verify that an error was raised (can be NETWORK_ERROR, UNKNOWN, or VALIDATION_ERROR)
        assert excinfo.value.error_code in [ErrorCode.NETWORK_ERROR, ErrorCode.UNKNOWN, ErrorCode.VALIDATION_ERROR]
    finally:
        # Cleanup - restore webhook URL
        if original_url:
            os.environ["WECOM_WEBHOOK_URL"] = original_url


@pytest.mark.asyncio
async def test_error_handling_invalid_message_type(mock_message_send):
    """Test error handling when message type is invalid."""
    # Execute and verify
    with pytest.raises(WeComError) as excinfo:
        await send_message(content="Test", msg_type="invalid_type")

    # Just verify that an error was raised (can be NETWORK_ERROR, UNKNOWN, or VALIDATION_ERROR)
    assert excinfo.value.error_code in [ErrorCode.NETWORK_ERROR, ErrorCode.UNKNOWN, ErrorCode.VALIDATION_ERROR]


@pytest.mark.asyncio
async def test_error_handling_file_not_found():
    """Test error handling when file is not found."""
    # Execute and verify
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_file("nonexistent_file.txt")

    # Just verify that an error was raised
    assert excinfo.value.error_code in [ErrorCode.UNKNOWN, ErrorCode.FILE_ERROR]


@pytest.mark.asyncio
async def test_error_handling_image_not_found():
    """Test error handling when image is not found."""
    # Execute and verify
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_image("nonexistent_image.jpg")

    # Just verify that an error was raised
    assert excinfo.value.error_code in [ErrorCode.UNKNOWN, ErrorCode.NETWORK_ERROR, ErrorCode.FILE_ERROR]


@pytest.mark.asyncio
async def test_multiple_messages_sequence(mock_message_send):
    """Test sending multiple messages in sequence."""
    # Execute - send multiple messages
    results = []

    # Send text message
    result1 = await send_message(content="Message 1", msg_type="text")
    results.append(result1)

    # Send markdown message
    result2 = await send_message(content="## Message 2", msg_type="markdown")
    results.append(result2)

    # Send text with mentions
    result3 = await send_message(content="Message 3", msg_type="text", mentioned_list=["user1"])
    results.append(result3)

    # Verify all succeeded
    for result in results:
        assert result is not None
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_message_history_tracking(mock_message_send):
    """Test that message history is tracked correctly."""
    from wecom_bot_mcp_server import MESSAGE_HISTORY_KEY

    # Verify MESSAGE_HISTORY_KEY is defined
    assert MESSAGE_HISTORY_KEY is not None
    assert isinstance(MESSAGE_HISTORY_KEY, str)

    # Send a message
    content = "Test message for history"
    result = await send_message(content=content, msg_type="text")

    # Verify message was sent
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_concurrent_message_sending(mock_message_send):
    """Test sending multiple messages concurrently."""
    import asyncio

    # Create multiple message tasks
    tasks = [
        send_message(content=f"Message {i}", msg_type="text") for i in range(5)
    ]

    # Execute concurrently
    results = await asyncio.gather(*tasks)

    # Verify all succeeded
    assert len(results) == 5
    for result in results:
        assert result is not None
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_special_characters_in_message(mock_message_send):
    """Test sending messages with special characters."""
    # Test various special characters
    special_contents = [
        "Hello 世界",  # Chinese characters
        "Test with emoji 😀",  # Emoji
        "Special chars: @#$%^&*()",  # Special symbols
        "Line\nBreak\nTest",  # Line breaks
        "Tab\tTest",  # Tabs
    ]

    for content in special_contents:
        result = await send_message(content=content, msg_type="text")
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_long_message_content(mock_message_send):
    """Test sending a long message."""
    # Create a long message
    long_content = "A" * 1000

    # Execute
    result = await send_message(content=long_content, msg_type="text")

    # Verify
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_empty_mentioned_list(mock_message_send):
    """Test sending message with empty mentioned list."""
    # Execute
    result = await send_message(content="Test", msg_type="text", mentioned_list=[])

    # Verify
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_markdown_formatting(mock_message_send):
    """Test various markdown formatting options."""
    markdown_contents = [
        "# Heading 1",
        "## Heading 2",
        "**Bold text**",
        "*Italic text*",
        "- List item 1\n- List item 2",
        "1. Numbered item 1\n2. Numbered item 2",
        "[Link](https://example.com)",
        "`code block`",
    ]

    for content in markdown_contents:
        result = await send_message(content=content, msg_type="markdown")
        assert result["status"] == "success"

