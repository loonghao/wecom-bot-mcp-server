"""Logging configuration for WeCom Bot MCP Server."""

# Import built-in modules
import os
from pathlib import Path
import sys
from typing import Any

# Import third-party modules
from loguru import logger
from platformdirs import user_log_dir

# Import local modules
from wecom_bot_mcp_server.app import APP_NAME


class LoggerWrapper:
    """Wrapper class to provide a logging.Logger-like interface for loguru."""

    def __init__(self, name: str):
        """Initialize logger wrapper with a name.

        Args:
            name: The name of the logger.

        """
        self.name = name

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).error(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).info(msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).warning(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an exception message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).exception(msg, *args, **kwargs)


def _parse_bool_env(name: str, default: bool = True) -> bool:
    """Parse boolean environment variable.

    Args:
        name: Environment variable name.
        default: Default value if not set.

    Returns:
        bool: Parsed boolean value.

    """
    value = os.getenv(name, "").lower()
    if value in ("false", "0", "no", "off", "disabled"):
        return False
    if value in ("true", "1", "yes", "on", "enabled"):
        return True
    return default


def _parse_size_env(name: str, default: str) -> str:
    """Parse size environment variable.

    Args:
        name: Environment variable name.
        default: Default value if not set.

    Returns:
        str: Size string (e.g., "10 MB", "1 GB").

    """
    return os.getenv(name, default)


def _parse_int_env(name: str, default: int) -> int:
    """Parse integer environment variable.

    Args:
        name: Environment variable name.
        default: Default value if not set.

    Returns:
        int: Parsed integer value.

    """
    value = os.getenv(name, "")
    if value.isdigit():
        return int(value)
    return default


# Constants
LOG_DIR = Path(user_log_dir(APP_NAME))
LOG_FILE = LOG_DIR / "mcp_wecom.log"
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan> - "
    "<level>{level}</level> - <level>{message}</level>"
)

# Environment variable configuration
# WECOM_LOG_ENABLED: Enable/disable file logging (default: true)
# WECOM_LOG_LEVEL: Log level (default: DEBUG)
# WECOM_LOG_MAX_SIZE: Max log file size before rotation (default: 10 MB)
# WECOM_LOG_RETENTION: Number of rotated log files to keep (default: 3)
# WECOM_LOG_CONSOLE: Enable/disable console logging (default: true)
LOG_ENABLED = _parse_bool_env("WECOM_LOG_ENABLED", True)
LOG_LEVEL = os.getenv("WECOM_LOG_LEVEL", os.getenv("MCP_LOG_LEVEL", "DEBUG")).upper()
LOG_MAX_SIZE = _parse_size_env("WECOM_LOG_MAX_SIZE", "10 MB")
LOG_RETENTION = _parse_int_env("WECOM_LOG_RETENTION", 3)
LOG_CONSOLE_ENABLED = _parse_bool_env("WECOM_LOG_CONSOLE", True)


def setup_logging() -> LoggerWrapper:
    """Configure logging settings for the application using loguru.

    Environment Variables:
        WECOM_LOG_ENABLED: Enable/disable file logging (default: true).
            Set to "false", "0", "no", "off", or "disabled" to disable file logging.
            This is useful for serverless environments with limited disk space.
        WECOM_LOG_LEVEL: Log level (default: DEBUG).
            Also supports legacy MCP_LOG_LEVEL for backward compatibility.
        WECOM_LOG_MAX_SIZE: Max log file size before rotation (default: "10 MB").
            Supports formats like "10 MB", "1 GB", "500 KB".
        WECOM_LOG_RETENTION: Number of rotated log files to keep (default: 3).
            Set to 0 to keep only the current log file.
        WECOM_LOG_CONSOLE: Enable/disable console logging (default: true).
            Set to "false" to disable console output.

    Returns:
        LoggerWrapper: Configured logger instance that provides a logging.Logger-like interface

    """
    # Remove any existing handlers
    logger.remove()

    # Add rotating file handler if enabled
    if LOG_ENABLED:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        logger.add(
            LOG_FILE,
            rotation=LOG_MAX_SIZE,
            retention=LOG_RETENTION,
            compression="zip",
            format=LOG_FORMAT,
            level=LOG_LEVEL,
            enqueue=True,
            encoding="utf-8",
        )

    # Add console handler if enabled
    if LOG_CONSOLE_ENABLED:
        logger.add(sys.stdout, format=LOG_FORMAT, level=LOG_LEVEL, enqueue=True)

    logger_wrapper = LoggerWrapper("mcp_wechat_server")

    if LOG_ENABLED:
        logger_wrapper.info(f"Log file location: {LOG_FILE}")
        logger_wrapper.info(f"Log rotation: {LOG_MAX_SIZE}, retention: {LOG_RETENTION} files")
    else:
        logger_wrapper.info("File logging disabled")

    return logger_wrapper
