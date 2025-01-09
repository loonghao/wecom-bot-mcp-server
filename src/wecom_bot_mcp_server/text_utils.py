"""Text utilities for handling Chinese characters and encoding issues.

This module provides utilities for handling Chinese text encoding and decoding,
ensuring proper handling of Chinese characters in different scenarios.
"""

# Import built-in modules
import codecs
import json
import logging
from typing import List

logger = logging.getLogger(__name__)

# Common Chinese encodings to try
CHINESE_ENCODINGS: List[str] = ["utf-8", "gbk", "gb2312", "gb18030"]


def fix_encoding(text: str) -> str:
    """Fix text encoding issues by trying different Chinese encodings.

    Args:
        text: The text to fix encoding for

    Returns:
        str: The text with fixed encoding
    """
    if not text:
        return text

    try:
        # First try to detect if the text is already properly encoded UTF-8
        try:
            text.encode("utf-8").decode("utf-8")
            return text
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

        # Try to decode as UTF-8 first
        try:
            return text.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

        # Try different Chinese encodings
        for encoding in CHINESE_ENCODINGS:
            try:
                return text.encode("latin1").decode(encoding)
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue

        # If all else fails, try using codecs with error handling
        return codecs.decode(codecs.encode(text, "utf-8", errors="replace"), "utf-8", errors="replace")
    except Exception as e:
        logger.error("Error fixing encoding: %s", e, exc_info=True)
        return text


def encode_text(text: str) -> str:
    """Encode text to ensure proper handling of Chinese characters.

    This function first fixes any encoding issues, then converts the text
    to a JSON string while preserving Chinese characters.

    Args:
        text: The text to encode

    Returns:
        str: The encoded text
    """
    if not text:
        return text

    try:
        # First fix encoding issues
        fixed_text = fix_encoding(text)
        logger.debug("Fixed text encoding: %s", fixed_text)

        # Convert fixed text to JSON string
        encoded = json.dumps(fixed_text, ensure_ascii=False)
        logger.debug("Encoded text: %s", encoded)
        return encoded
    except Exception as e:
        logger.error("Error encoding text: %s", e, exc_info=True)
        return text


def decode_text(text: str) -> str:
    """Decode text from JSON format while handling Chinese characters.

    This function attempts to decode JSON-encoded text and fix any
    encoding issues with the decoded result.

    Args:
        text: The text to decode

    Returns:
        str: The decoded text
    """
    if not text:
        return text

    try:
        # Check if text is JSON encoded
        if text.startswith('"') and text.endswith('"'):
            decoded = json.loads(text)
            logger.debug("Decoded JSON text: %s", decoded)
            return fix_encoding(decoded)

        # If not JSON, just fix encoding
        fixed = fix_encoding(text)
        logger.debug("Fixed non-JSON text encoding: %s", fixed)
        return fixed
    except Exception as e:
        logger.error("Error decoding text: %s", e, exc_info=True)
        return text
