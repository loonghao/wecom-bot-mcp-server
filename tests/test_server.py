"""Tests for WeCom Bot MCP Server Implementation.

This module contains unit tests for the WeCom bot server implementation.
It tests message sending functionality, message history management, and text encoding.
"""

# Import built-in modules
from unittest.mock import MagicMock
from unittest.mock import patch

# Import third-party modules
from PIL import Image
import httpx
import pytest

# Import local modules
from wecom_bot_mcp_server.server import encode_text
from wecom_bot_mcp_server.server import get_message_history
from wecom_bot_mcp_server.server import message_history
from wecom_bot_mcp_server.server import send_message
from wecom_bot_mcp_server.server import send_wecom_file
from wecom_bot_mcp_server.server import send_wecom_image


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch) -> None:
    """Set up test environment before each test.

    Sets up required environment variables and cleans up message history.

    Args:
        monkeypatch: pytest fixture for modifying environment

    """
    monkeypatch.setenv("WECOM_WEBHOOK_URL", "https://mock.wecom.api/webhook")
    yield


@pytest.fixture(autouse=True)
def clear_message_history() -> None:
    """Clear message history before each test."""
    message_history.clear()
    yield


@pytest.mark.asyncio
async def test_send_message_success() -> None:
    """Test successful message sending.

    Tests that:
    1. Message is sent successfully
    2. Message is added to history
    3. Correct response is returned
    """
    test_message = "Test message"

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}

    async def mock_send_async(self, service, params):
        # Verify that the message content is properly encoded
        assert params["msg_type"] == "markdown"
        assert params["content"] == '"Test message"'
        return mock_response

    with patch("notify_bridge.NotifyBridge.send_async", new=mock_send_async):
        result = await send_message(test_message)
        assert result == "Message sent successfully"
        assert len(message_history) == 1
        assert message_history[0]["role"] == "assistant"
        assert message_history[0]["content"] == test_message


@pytest.mark.asyncio
async def test_send_message_empty_content() -> None:
    """Test sending empty message content.

    Verifies that attempting to send empty content raises ValueError.
    """
    with pytest.raises(ValueError, match="Message content cannot be empty"):
        await send_message("")


@pytest.mark.asyncio
async def test_send_message_api_error() -> None:
    """Test handling of API errors.

    Tests error handling for:
    1. HTTP error response
    2. WeChat API error response
    """
    test_message = "Test message"

    # Mock error response
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    async def mock_post(*args, **kwargs):
        return mock_response

    with patch("httpx.AsyncClient.post", new=mock_post), pytest.raises(ValueError, match="Failed to send message"):
        await send_message(test_message)


def test_get_message_history_empty() -> None:
    """Test getting empty message history."""
    assert get_message_history() == ""


def test_get_message_history_with_messages() -> None:
    """Test getting message history with messages.

    Tests that:
    1. Messages are correctly formatted
    2. Multiple messages are separated by newlines
    """
    message_history.extend(
        [{"role": "assistant", "content": "Message 1"}, {"role": "assistant", "content": "Message 2"}]
    )

    history = get_message_history()
    assert "Message 1" in history
    assert "Message 2" in history
    assert history.count("\n") == 1  # One newline between two messages


def test_encode_text_ascii() -> None:
    """Test encoding simple ASCII text."""
    text = "Hello, World!"
    result = encode_text(text)
    assert result == '"Hello, World!"'


def test_encode_text_chinese() -> None:
    """Test encoding Chinese characters."""
    text = "你好,世界!"
    result = encode_text(text)
    assert result == '"你好,世界!"'


def test_encode_text_mixed() -> None:
    """Test encoding mixed ASCII and Chinese text."""
    text = "Hello 你好 World 世界!"
    result = encode_text(text)
    assert result == '"Hello 你好 World 世界!"'


def test_encode_text_special_chars() -> None:
    """Test encoding text with special characters."""
    text = "Special ™ ® © ☺ ♥ characters"
    result = encode_text(text)
    assert result == '"Special ™ ® © ☺ ♥ characters"'


def test_encode_text_emoji() -> None:
    """Test encoding text with emoji."""
    text = "Hello 👋 World 🌍"
    result = encode_text(text)
    assert result == '"Hello 👋 World 🌍"'


def test_encode_text_error_handling() -> None:
    """Test error handling in encode_text."""
    # Mock ftfy.fix_text to raise an exception
    with patch("ftfy.fix_text", side_effect=Exception("Test error")):
        text = "Test text"
        with pytest.raises(ValueError, match="Failed to encode text: Test error"):
            encode_text(text)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", '""'),  # Empty string
        (" ", '" "'),  # Space only
        ("Hello\nWorld", '"Hello\\nWorld"'),  # Newline
        ("Tab\tTest", '"Tab\\tTest"'),  # Tab
        ('Quote"Test', '"Quote\\"Test"'),  # Quote
    ],
)
def test_encode_text_edge_cases(text: str, expected: str) -> None:
    """Test encoding edge cases.

    Args:
        text: Input text to test
        expected: Expected encoded output

    """
    result = encode_text(text)
    assert result == expected


@pytest.mark.asyncio
async def test_send_wecom_file_success(tmp_path) -> None:
    """Test successful file sending.

    Tests that:
    1. File is sent successfully
    2. Correct response is returned
    """
    # Create a temporary test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test content")

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}

    async def mock_send_async(self, service, params):
        return mock_response

    with patch("notify_bridge.NotifyBridge.send_async", new=mock_send_async):
        result = await send_wecom_file(str(test_file))
        assert result == "File sent successfully"


@pytest.mark.asyncio
async def test_send_wecom_file_not_found() -> None:
    """Test sending non-existent file."""
    with pytest.raises(ValueError, match="File not found"):
        await send_wecom_file("nonexistent.txt")


@pytest.mark.asyncio
async def test_send_wecom_image_invalid_format(tmp_path) -> None:
    """Test sending image with invalid format."""
    # Create a text file with .txt extension
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is not an image")

    with pytest.raises(ValueError, match="Failed to open image:"):
        await send_wecom_image(str(test_file))


@pytest.mark.asyncio
async def test_send_wecom_image_from_url(tmp_path) -> None:
    """Test sending image from URL."""
    # Mock HTTP response for image download
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake image data"

    # Mock successful response for image sending
    mock_send_response = MagicMock()
    mock_send_response.status_code = 200
    mock_send_response.json.return_value = {"errcode": 0, "errmsg": "ok"}

    # Create a real PNG file for the test
    test_image = tmp_path / "test.png"
    img = Image.new("RGB", (60, 30), color="red")
    img.save(test_image)

    async def mock_get(*args, **kwargs):
        # Return the real PNG file content
        with open(test_image, "rb") as f:
            mock_response.content = f.read()
        return mock_response

    async def mock_send_async(self, service, params):
        return mock_send_response

    with (
        patch("httpx.AsyncClient.get", new=mock_get),
        patch("notify_bridge.NotifyBridge.send_async", new=mock_send_async),
    ):
        result = await send_wecom_image("https://example.com/test.png")
        assert result == "Image sent successfully"


@pytest.mark.asyncio
async def test_send_wecom_image_svg_conversion(tmp_path) -> None:
    """Test sending SVG image with conversion."""
    try:
        # Only import renderPM since we're mocking svg2rlg
        # Import third-party modules
        from reportlab.graphics import renderPM  # noqa: F401
    except ImportError:
        pytest.skip("svglib not available, skipping SVG conversion test")

    # Create a test SVG file
    test_svg = tmp_path / "test.svg"
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
        <rect width="100" height="100" fill="red"/>
    </svg>"""
    test_svg.write_text(svg_content)

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}

    async def mock_send_async(self, service, params):
        return mock_response

    # Mock svg2rlg and renderPM
    def mock_svg2rlg(path):
        # Import third-party modules
        from reportlab.graphics.shapes import Drawing

        return Drawing(100, 100)

    def mock_draw_to_file(drawing, path, fmt):
        img = Image.new("RGB", (100, 100), color="red")
        img.save(path)

    with (
        patch("notify_bridge.NotifyBridge.send_async", new=mock_send_async),
        patch("svglib.svglib.svg2rlg", new=mock_svg2rlg),
        patch("reportlab.graphics.renderPM.drawToFile", new=mock_draw_to_file),
    ):
        result = await send_wecom_image(str(test_svg))
        assert result == "Image sent successfully"


@pytest.mark.asyncio
async def test_send_wecom_image_url_download_error() -> None:
    """Test error handling when downloading image from URL fails."""

    async def mock_get(*args, **kwargs):
        raise httpx.RequestError("Failed to download")

    with (
        patch("httpx.AsyncClient.get", side_effect=mock_get),
        pytest.raises(ValueError, match="Failed to download image"),
    ):
        await send_wecom_image("https://example.com/test.png")


@pytest.mark.asyncio
async def test_send_wecom_image_not_found() -> None:
    """Test sending non-existent image."""
    with pytest.raises(ValueError, match="Image not found"):
        await send_wecom_image("nonexistent.png")
