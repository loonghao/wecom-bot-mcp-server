"""Logger configuration for WeCom Bot MCP Server.

This module provides logging configuration for the WeCom Bot MCP Server.
It sets up both console and file logging with appropriate formatting.
"""

# Import built-in modules
import logging
import os
from pathlib import Path
from typing import TextIO

# Import third-party modules
from concurrent_log_handler import ConcurrentRotatingFileHandler  # type: ignore
from platformdirs import PlatformDirs

# Import local modules
from wecom_bot_mcp_server.constants import APP_AUTHOR, APP_NAME


def setup_logger(name: str, log_file: str | None = None) -> logging.Logger:
    """Setup and configure logger with both console and file output.

    Args:
        name: Logger name
        log_file: Optional path to log file. If not provided, will use default location.

    Returns:
        logging.Logger: Configured logger instance

    Raises:
        OSError: If unable to create log directory
        Exception: If file handler setup fails
    """
    # Get log level from environment variable
    log_level_str: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level: int = getattr(logging, log_level_str, logging.INFO)

    # Create logger
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicate logs
    logger.handlers.clear()

    # Create formatters
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    formatter: logging.Formatter = logging.Formatter(log_format)

    # Create console handler
    console_handler: logging.StreamHandler[TextIO] = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler
    if log_file is None:
        # Use default log file location
        platform_dirs = PlatformDirs(APP_NAME, APP_AUTHOR)
        log_dir = Path(platform_dirs.user_log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = str(log_dir / f"{name}.log")

    # Create rotating file handler
    file_handler = ConcurrentRotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log initial messages
    logger.info("Logger setup completed - This is an info message")
    logger.debug("Logger debug level enabled")
    logger.info(f"Log file location: {log_file}")

    return logger
