"""Test cases for utils module."""

# Import built-in modules
import os
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.utils import encode_text
from wecom_bot_mcp_server.utils import get_webhook_url


def test_get_webhook_url_success():
    """Test retrieving webhook URL with valid environment variable."""
    test_url = "https://test-webhook.example.com"

    with patch.dict(os.environ, {"WECOM_WEBHOOK_URL": test_url}, clear=False):
        # Clear the lru_cache to ensure we get a fresh URL
        get_webhook_url.cache_clear()

        # Get the webhook URL
        url = get_webhook_url()

        # Verify the URL matches what we set
        assert url == test_url


def test_get_webhook_url_missing():
    """Test retrieving webhook URL with missing environment variable."""
    with patch.dict(os.environ, {}, clear=False):
        # Ensure WECOM_WEBHOOK_URL is not set
        if "WECOM_WEBHOOK_URL" in os.environ:
            del os.environ["WECOM_WEBHOOK_URL"]

        # Clear the lru_cache to ensure we get a fresh result
        get_webhook_url.cache_clear()

        # Verify that an exception is raised
        with pytest.raises(WeComError) as exc_info:
            get_webhook_url()

        # Check error message
        assert "WECOM_WEBHOOK_URL environment variable not set" in str(exc_info.value)


def test_encode_text_normal():
    """Test encoding normal text."""
    input_text = "Hello, world!"
    output_text = encode_text(input_text)

    # Output should match input for normal text
    assert output_text == input_text


def test_encode_text_with_special_chars():
    """Test encoding text with special characters."""
    input_text = 'Text with "quotes" and \\backslashes\\nand newlines'
    output_text = encode_text(input_text)

    # Verify special characters are escaped
    assert '"' not in output_text.replace('\\"', "")  # 检查原始引号已被转义
    assert '\\"' in output_text
    assert "\\\\" in output_text
    assert "\\n" in output_text


def test_encode_text_unicode():
    """Test encoding text with Unicode characters."""
    input_text = "Unicode: and emojis: "
    output_text = encode_text(input_text)

    # Unicode characters should be preserved
    assert "" in output_text
    assert "" in output_text


def test_encode_text_complex_formatting():
    """Test encoding complex text with multiple formatting elements."""
    input_text = "# Heading\n\n- Item 1\n- Item 2\n\n```code\nprint('hello')\n```"
    output_text = encode_text(input_text)

    # Newlines should be escaped
    assert output_text.count("\\n") >= 6

    # Original content should be preserved semantically
    assert "# Heading" in output_text
    assert "- Item" in output_text
    assert "print('hello')" in output_text


@patch("logging.getLogger")
def test_encode_text_error(mock_get_logger):
    """Test error handling in encode_text."""
    # Setup mock logger
    mock_logger = mock_get_logger.return_value

    # Create a scenario that would cause an error in ftfy
    with patch("ftfy.fix_text", side_effect=Exception("Test error")):
        # Verify exception is raised
        with pytest.raises(ValueError) as exc_info:
            encode_text("Test text")

        # Check error message
        assert "Failed to encode text" in str(exc_info.value)
        assert "Test error" in str(exc_info.value)

        # Verify error was logged
        mock_logger.error.assert_called_once()
