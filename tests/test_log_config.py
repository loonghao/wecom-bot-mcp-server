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


@pytest.fixture
def logger_mock():
    """Create a mocked logger."""
    with patch("wecom_bot_mcp_server.log_config.logger") as mock_logger:
        mock_bind = MagicMock()
        mock_logger.bind.return_value = mock_bind
        yield mock_logger, mock_bind


def test_logger_wrapper_init():
    """Test LoggerWrapper initialization."""
    wrapper = LoggerWrapper("test_logger")
    assert wrapper.name == "test_logger"


def test_logger_wrapper_error(logger_mock):
    """Test LoggerWrapper.error method."""
    mock_logger, mock_bind = logger_mock
    wrapper = LoggerWrapper("test_logger")

    wrapper.error("Error message", extra_arg="value")

    mock_logger.bind.assert_called_once_with(name="test_logger")
    mock_bind.error.assert_called_once_with("Error message", extra_arg="value")


def test_logger_wrapper_info(logger_mock):
    """Test LoggerWrapper.info method."""
    mock_logger, mock_bind = logger_mock
    wrapper = LoggerWrapper("test_logger")

    wrapper.info("Info message", extra_arg="value")

    mock_logger.bind.assert_called_once_with(name="test_logger")
    mock_bind.info.assert_called_once_with("Info message", extra_arg="value")


def test_logger_wrapper_debug(logger_mock):
    """Test LoggerWrapper.debug method."""
    mock_logger, mock_bind = logger_mock
    wrapper = LoggerWrapper("test_logger")

    wrapper.debug("Debug message", extra_arg="value")

    mock_logger.bind.assert_called_once_with(name="test_logger")
    mock_bind.debug.assert_called_once_with("Debug message", extra_arg="value")


def test_logger_wrapper_warning(logger_mock):
    """Test LoggerWrapper.warning method."""
    mock_logger, mock_bind = logger_mock
    wrapper = LoggerWrapper("test_logger")

    wrapper.warning("Warning message", extra_arg="value")

    mock_logger.bind.assert_called_once_with(name="test_logger")
    mock_bind.warning.assert_called_once_with("Warning message", extra_arg="value")


def test_logger_wrapper_critical(logger_mock):
    """Test LoggerWrapper.critical method."""
    mock_logger, mock_bind = logger_mock
    wrapper = LoggerWrapper("test_logger")

    wrapper.critical("Critical message", extra_arg="value")

    mock_logger.bind.assert_called_once_with(name="test_logger")
    mock_bind.critical.assert_called_once_with("Critical message", extra_arg="value")


def test_logger_wrapper_exception(logger_mock):
    """Test LoggerWrapper.exception method."""
    mock_logger, mock_bind = logger_mock
    wrapper = LoggerWrapper("test_logger")

    wrapper.exception("Exception message", extra_arg="value")

    mock_logger.bind.assert_called_once_with(name="test_logger")
    mock_bind.exception.assert_called_once_with("Exception message", extra_arg="value")


@patch("wecom_bot_mcp_server.log_config.LOG_DIR")
@patch("wecom_bot_mcp_server.log_config.logger")
def test_setup_logging(mock_logger, mock_log_dir):
    """Test setup_logging function."""
    # Setup mocks
    mock_log_dir.__truediv__.return_value = "mocked_log_file.log"

    # Test with default settings
    with patch.dict(os.environ, {}, clear=True):
        with patch("wecom_bot_mcp_server.log_config.LOG_LEVEL", "DEBUG"):
            logger_wrapper = setup_logging()

            # Verify logger is properly configured
            assert isinstance(logger_wrapper, LoggerWrapper)

            # 验证创建目录
            mock_log_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)

            # 验证remove被调用
            mock_logger.remove.assert_called_once()

            # Verify add was called twice (file and stdout)
            assert mock_logger.add.call_count == 2

            # 验证日志级别
            assert mock_logger.add.call_args_list[0][1]["level"] == "DEBUG"


@patch("wecom_bot_mcp_server.log_config.LOG_DIR")
@patch("wecom_bot_mcp_server.log_config.logger")
def test_setup_logging_with_custom_level(mock_logger, mock_log_dir):
    """Test setup_logging function with custom log level."""
    # Setup mocks
    mock_log_dir.__truediv__.return_value = "mocked_log_file.log"

    # Test with custom log level
    with patch.dict(os.environ, {"MCP_LOG_LEVEL": "ERROR"}, clear=True):
        with patch("wecom_bot_mcp_server.log_config.LOG_LEVEL", "ERROR"):
            logger_wrapper = setup_logging()

            # Verify logger is properly configured
            assert isinstance(logger_wrapper, LoggerWrapper)

            # Check file handler was added with correct level
            assert mock_logger.add.call_args_list[0][1]["level"] == "ERROR"

            # Check console handler was added with correct level
            assert mock_logger.add.call_args_list[1][1]["level"] == "ERROR"
