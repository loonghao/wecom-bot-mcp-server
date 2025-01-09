"""Tests for text utilities."""

import pytest

from wecom_bot_mcp_server.text_utils import decode_text, encode_text, fix_encoding


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("你好", "你好"),  # Simple Chinese text
        ("Hello世界", "Hello世界"),  # Mixed English and Chinese
        ("", ""),  # Empty string
        (None, None),  # None value
        ("测试test测试", "测试test测试"),  # Mixed Chinese and English
        ("🎉你好", "🎉你好"),  # Emoji and Chinese
    ],
)
def test_fix_encoding(input_text: str, expected: str) -> None:
    """Test fix_encoding function with various inputs."""
    if input_text is None:
        assert fix_encoding(input_text) is None  # type: ignore
    else:
        assert fix_encoding(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("你好", '"你好"'),  # Simple Chinese text
        ("Hello世界", '"Hello世界"'),  # Mixed English and Chinese
        ("", ""),  # Empty string
        (None, None),  # None value
        ("测试test测试", '"测试test测试"'),  # Mixed Chinese and English
        ("🎉你好", '"🎉你好"'),  # Emoji and Chinese
    ],
)
def test_encode_text(input_text: str, expected: str) -> None:
    """Test encode_text function with various inputs."""
    if input_text is None:
        assert encode_text(input_text) is None  # type: ignore
    else:
        assert encode_text(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ('"你好"', "你好"),  # JSON encoded Chinese text
        ('"Hello世界"', "Hello世界"),  # JSON encoded mixed text
        ("", ""),  # Empty string
        (None, None),  # None value
        ("测试test测试", "测试test测试"),  # Non-JSON text
        ('"🎉你好"', "🎉你好"),  # JSON encoded emoji and Chinese
    ],
)
def test_decode_text(input_text: str, expected: str) -> None:
    """Test decode_text function with various inputs."""
    if input_text is None:
        assert decode_text(input_text) is None  # type: ignore
    else:
        assert decode_text(input_text) == expected


def test_encoding_decoding_roundtrip() -> None:
    """Test that encoding and then decoding preserves the original text."""
    original_texts = [
        "你好",
        "Hello世界",
        "测试test测试",
        "🎉你好",
        "这是一个很长的中文文本，包含标点符号！？。，",
    ]

    for text in original_texts:
        encoded = encode_text(text)
        decoded = decode_text(encoded)
        assert decoded == text, f"Round trip failed for: {text}"
