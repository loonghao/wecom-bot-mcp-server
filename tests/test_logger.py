"""Tests for logger configuration module."""

# Import built-in modules
import logging
from io import StringIO

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.logger import setup_logger


@pytest.fixture
def cleanup_logger():
    """Clean up logger after each test."""
    yield
    logger = logging.getLogger("test_logger")
    logger.handlers.clear()


def test_logger_creation_with_default_dir(cleanup_logger):
    """Test logger creation with default directory."""
    logger = setup_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0


def test_logger_creation_with_custom_level(cleanup_logger, monkeypatch):
    """Test logger creation with custom log level."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    logger = setup_logger("test_logger")
    assert logger.level == logging.DEBUG


def test_logger_output(cleanup_logger, tmp_path):
    """Test logger output to file and console."""
    log_file = tmp_path / "test.log"

    # Create a StringIO object to capture console output
    console_output = StringIO()
    handler = logging.StreamHandler(console_output)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger = setup_logger("test_logger", log_file=str(log_file))
    # Add our test handler while keeping the existing handlers
    logger.addHandler(handler)

    test_message = "Test log message"
    logger.info(test_message)

    # Check console output
    console_output.seek(0)
    assert test_message in console_output.getvalue()

    # Check file output
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "Test log message" in log_content
