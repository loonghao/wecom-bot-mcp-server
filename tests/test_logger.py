"""Test cases for logger configuration module."""

# Import built-in modules
import logging
import shutil
from pathlib import Path

# Import third-party modules
import pytest
from platformdirs import PlatformDirs

# Import local modules
from wecom_bot_mcp_server.logger import setup_logger


@pytest.fixture
def temp_log_dir(tmp_path):
    """Create a temporary directory for log files."""
    log_dir = tmp_path / "test_logs"
    log_dir.mkdir()
    yield log_dir
    # Clean up
    shutil.rmtree(log_dir)

def test_logger_creation_with_custom_dir(temp_log_dir):
    """Test logger creation with custom directory."""
    logger_name = "test_logger"
    logger = setup_logger(logger_name, str(temp_log_dir))

    # Verify logger is properly configured
    assert logger.name == logger_name
    assert logger.level == logging.INFO

    # Verify handlers are properly set up
    handlers = logger.handlers
    assert len(handlers) == 2  # Console and file handler

    # Verify log file is created
    log_file = temp_log_dir / f"{logger_name}.log"
    assert log_file.exists()

def test_logger_creation_with_default_dir():
    """Test logger creation with default platform directory."""
    logger_name = "test_default_dir"
    logger = setup_logger(logger_name)

    # Get expected log directory
    dirs = PlatformDirs("wecom-bot-mcp-server", appauthor="codeium")
    expected_log_dir = Path(dirs.user_log_dir)

    # Verify log file is created in platform directory
    log_file = expected_log_dir / f"{logger_name}.log"
    assert log_file.exists()

    # Clean up
    log_file.unlink()
    try:
        expected_log_dir.rmdir()  # Only remove if empty
    except OSError:
        pass  # Directory not empty, leave it

def test_logger_output(temp_log_dir):
    """Test logger output to both console and file."""
    logger = setup_logger("test_output", str(temp_log_dir))
    test_message = "Test log message"
    logger.info(test_message)

    # Verify message is written to file
    log_file = temp_log_dir / "test_output.log"
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
        assert test_message in log_content
