"""Tests for Markdown formatting and encoding."""

# Import built-in modules
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.message import _prepare_message_content
from wecom_bot_mcp_server.message import send_message
from wecom_bot_mcp_server.utils import encode_text


def test_encode_markdown_basic():
    """Test encoding basic Markdown formatting."""
    markdown_text = "# Heading\n\n**Bold text** and *italic text*"
    encoded = encode_text(markdown_text)

    # Verify Markdown syntax is preserved
    assert "# Heading" in encoded
    assert "**Bold text**" in encoded
    assert "*italic text*" in encoded
    assert "\\n" in encoded  # Newlines should be escaped


def test_encode_markdown_code_blocks():
    """Test encoding Markdown code blocks."""
    markdown_text = "```python\nprint('Hello world')\n```"
    encoded = encode_text(markdown_text)

    # Verify code block syntax is preserved
    assert "```python" in encoded
    assert "print('Hello world')" in encoded
    assert "```" in encoded
    assert encoded.count("\\n") == 2  # Two newlines should be escaped


def test_encode_markdown_tables():
    """Test encoding Markdown tables."""
    markdown_text = "|Header 1|Header 2|\n|--------|--------|"
    encoded = encode_text(markdown_text)

    # Verify table syntax is preserved
    assert "|Header 1|Header 2|" in encoded
    assert "|--------|--------|" in encoded
    assert "\\n" in encoded  # Newline should be escaped


def test_encode_markdown_with_special_chars():
    """Test encoding Markdown with special characters."""
    markdown_text = '# Heading with "quotes" and \\backslashes'
    encoded = encode_text(markdown_text)

    # Verify special characters are properly escaped
    assert '\\"quotes\\"' in encoded  # Double quotes should be escaped
    assert "\\\\backslashes" in encoded  # Backslashes should be escaped


def test_encode_markdown_with_links():
    """Test encoding Markdown links."""
    markdown_text = "[Link text](https://example.com)"
    encoded = encode_text(markdown_text)

    # Verify link syntax is preserved
    assert "[Link text]" in encoded
    assert "(https://example.com)" in encoded


def test_encode_markdown_with_images():
    """Test encoding Markdown image syntax."""
    markdown_text = "![Alt text](https://example.com/image.png)"
    encoded = encode_text(markdown_text)

    # Verify image syntax is preserved
    assert "![Alt text]" in encoded
    assert "(https://example.com/image.png)" in encoded


def test_encode_markdown_nested_formatting():
    """Test encoding nested Markdown formatting."""
    markdown_text = "# **Bold heading** with *italic* and `code`"
    encoded = encode_text(markdown_text)

    # Verify nested formatting is preserved
    assert "# **Bold heading**" in encoded
    assert "*italic*" in encoded
    assert "`code`" in encoded




def test_encode_markdown_v2_preserves_newlines_and_tabs():
    """Test encoding Markdown v2 preserves newlines and tabs."""
    markdown_text = "# Heading\n\nLine 2 with\ttab"
    encoded = encode_text(markdown_text, "markdown_v2")

    # Newlines and tabs should be preserved (not escaped as \n / \t)
    assert "\n" in encoded
    assert "\t" in encoded
    assert "\\n" not in encoded
    assert "\\t" not in encoded

@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.encode_text")
async def test_prepare_markdown_message(mock_encode_text):
    """Test preparing Markdown message content."""
    # Setup mock
    mock_encode_text.return_value = "Encoded markdown"

    # Call function
    result = await _prepare_message_content("# Test markdown")

    # Assertions
    assert result == "Encoded markdown"
    mock_encode_text.assert_called_once_with("# Test markdown", "text")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.encode_text")
async def test_prepare_explicit_markdown_message(mock_encode_text):
    """Test preparing explicit Markdown message content."""
    # Setup mock
    mock_encode_text.return_value = "Encoded markdown"

    # Call function with explicit markdown type
    result = await _prepare_message_content("# Test markdown", msg_type="markdown")

    # Assertions
    assert result == "Encoded markdown"
    mock_encode_text.assert_called_once_with("# Test markdown", "markdown")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.get_webhook_url")
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_markdown_message(mock_notify_bridge, mock_get_webhook_url):
    """Test sending markdown message with proper URL."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create markdown content with various elements
    markdown_content = "# Heading\n\n- Item 1\n- Item 2\n\n```code\nprint('hello')\n```"

    # Call function
    result = await send_message(markdown_content, "markdown")

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"

    # Verify the message was sent with the correct parameters
    mock_nb_instance.send_async.assert_called_once()
    call_args = mock_nb_instance.send_async.call_args[0][1]
    assert call_args["base_url"] == "https://example.com/webhook"
    assert call_args["msg_type"] == "markdown"

    # Verify content was properly encoded (not double-escaped)
    assert "# Heading" in call_args["content"]
    assert "- Item" in call_args["content"]
    assert "```code" in call_args["content"]
    assert "print('hello')" in call_args["content"]

    # Markdown should preserve newlines (not escaped as \n)
    assert "\n" in call_args["content"]
    assert "\\n" not in call_args["content"]


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.get_webhook_url")
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_markdown_v2_message(mock_notify_bridge, mock_get_webhook_url):
    """Test sending markdown_v2 message with proper URL."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    markdown_content = "# Heading\n\n- Item 1\n- Item 2\n\n![Alt](https://example.com/image.png)"

    # Call function
    result = await send_message(markdown_content, "markdown_v2")

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"

    # Verify the message was sent with the correct parameters
    mock_nb_instance.send_async.assert_called_once()
    call_args = mock_nb_instance.send_async.call_args[0][1]
    assert call_args["base_url"] == "https://example.com/webhook"
    assert call_args["msg_type"] == "markdown_v2"

    # Markdown v2 should preserve newlines (not escaped as \n)
    assert "\n" in call_args["content"]
    assert "\\n" not in call_args["content"]
