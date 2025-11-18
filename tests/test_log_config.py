"""Test cases for log_config module."""

# Import built-in modules
import os
from unittest.mock import MagicMock
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.log_config import LoggerWrapper
from wecom_bot_mcp_server.log_config import setup_logging


def test_logger_wrapper_init():
    """Test LoggerWrapper initialization."""
    wrapper = LoggerWrapper("test_logger")
    assert wrapper.name == "test_logger"


def test_logger_wrapper_error():
    """Test LoggerWrapper.error method."""
    wrapper = LoggerWrapper("test_logger")
    # Just verify it doesn't raise an exception
    wrapper.error("Error message", extra_arg="value")


def test_logger_wrapper_info():
    """Test LoggerWrapper.info method."""
    wrapper = LoggerWrapper("test_logger")
    # Just verify it doesn't raise an exception
    wrapper.info("Info message", extra_arg="value")


def test_logger_wrapper_debug():
    """Test LoggerWrapper.debug method."""
    wrapper = LoggerWrapper("test_logger")
    # Just verify it doesn't raise an exception
    wrapper.debug("Debug message", extra_arg="value")


def test_logger_wrapper_warning():
    """Test LoggerWrapper.warning method."""
    wrapper = LoggerWrapper("test_logger")
    # Just verify it doesn't raise an exception
    wrapper.warning("Warning message", extra_arg="value")


def test_logger_wrapper_critical():
    """Test LoggerWrapper.critical method."""
    wrapper = LoggerWrapper("test_logger")
    # Just verify it doesn't raise an exception
    wrapper.critical("Critical message", extra_arg="value")


def test_logger_wrapper_exception():
    """Test LoggerWrapper.exception method."""
    wrapper = LoggerWrapper("test_logger")
    # Just verify it doesn't raise an exception
    try:
        raise ValueError("Test exception")
    except ValueError:
        wrapper.exception("Exception message", extra_arg="value")


def test_setup_logging():
    """Test setup_logging function."""
    # Test with default settings - just verify it returns a LoggerWrapper
    logger_wrapper = setup_logging()

    # Verify logger is properly configured
    assert isinstance(logger_wrapper, LoggerWrapper)
    assert logger_wrapper.name == "mcp_wechat_server"


def test_setup_logging_with_custom_level():
    """Test setup_logging function with custom log level."""
    # Test with custom log level
    with patch.dict(os.environ, {"MCP_LOG_LEVEL": "ERROR"}, clear=True):
        # Re-import to pick up the new environment variable
        # Import built-in modules
        from importlib import reload

        # Import local modules
        import wecom_bot_mcp_server.log_config as log_config_module

        reload(log_config_module)

        logger_wrapper = log_config_module.setup_logging()

        # Verify logger is properly configured
        assert isinstance(logger_wrapper, log_config_module.LoggerWrapper)
        assert logger_wrapper.name == "mcp_wechat_server"
