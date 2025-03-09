"""Tests for Markdown formatting and encoding."""

# Import built-in modules
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.message import _prepare_message_content
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
