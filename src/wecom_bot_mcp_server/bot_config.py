"""Multi-bot configuration management for WeCom Bot MCP Server.

This module provides support for configuring and managing multiple WeCom bots.
It maintains backward compatibility with the single WECOM_WEBHOOK_URL environment
variable while adding support for multiple bots via WECOM_BOTS configuration.

Configuration Methods:
1. Single bot (backward compatible):
   - Set WECOM_WEBHOOK_URL environment variable

2. Multiple bots:
   - Set WECOM_BOTS environment variable as JSON:
     WECOM_BOTS='{"bot1": {"name": "Alert Bot", "webhook_url": "https://..."}, ...}'
   - Or set individual WECOM_BOT_<NAME>_URL variables:
     WECOM_BOT_ALERT_URL="https://..."
     WECOM_BOT_NOTIFY_URL="https://..."

3. Combined mode:
   - WECOM_WEBHOOK_URL becomes the "default" bot
   - Additional bots can be configured via WECOM_BOTS or WECOM_BOT_<NAME>_URL
"""

# Import built-in modules
from dataclasses import dataclass
from dataclasses import field
from functools import lru_cache
import json
import os
import re
from typing import Any

# Import third-party modules
from loguru import logger

# Import local modules
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError

# Constants
DEFAULT_BOT_NAME = "default"
ENV_WEBHOOK_URL = "WECOM_WEBHOOK_URL"
ENV_BOTS_CONFIG = "WECOM_BOTS"
ENV_BOT_URL_PATTERN = re.compile(r"^WECOM_BOT_(\w+)_URL$")


@dataclass
class BotConfig:
    """Configuration for a single WeCom bot.

    Attributes:
        name: Human-readable name for the bot (e.g., "Alert Bot", "CI Notify")
        webhook_url: The webhook URL for sending messages
        description: Optional description of the bot's purpose

    """

    name: str
    webhook_url: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the bot configuration after initialization."""
        if not self.webhook_url:
            raise WeComError(
                f"Bot '{self.name}' has empty webhook_url",
                ErrorCode.VALIDATION_ERROR,
            )
        if not self.webhook_url.startswith(("http://", "https://")):
            raise WeComError(
                f"Bot '{self.name}' webhook_url must start with 'http://' or 'https://'. Got: '{self.webhook_url}'",
                ErrorCode.VALIDATION_ERROR,
            )


class BotRegistry:
    """Registry for managing multiple WeCom bots.

    This class provides methods to register, retrieve, and list bots.
    It automatically loads configuration from environment variables.
    """

    def __init__(self) -> None:
        """Initialize the bot registry."""
        self._bots: dict[str, BotConfig] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        """Ensure bots are loaded from environment."""
        if not self._loaded:
            self._load_from_environment()
            self._loaded = True

    def _load_from_environment(self) -> None:
        """Load bot configurations from environment variables.

        Loading priority:
        1. WECOM_WEBHOOK_URL -> "default" bot (backward compatible)
        2. WECOM_BOTS JSON -> multiple bots
        3. WECOM_BOT_<NAME>_URL -> individual bot URLs
        """
        # 1. Load default bot from WECOM_WEBHOOK_URL (backward compatible)
        default_url = os.getenv(ENV_WEBHOOK_URL)
        if default_url:
            try:
                self._bots[DEFAULT_BOT_NAME] = BotConfig(
                    name=DEFAULT_BOT_NAME,
                    webhook_url=default_url.strip(),
                    description="Default bot (from WECOM_WEBHOOK_URL)",
                )
                logger.debug(f"Loaded default bot from {ENV_WEBHOOK_URL}")
            except WeComError as e:
                logger.warning(f"Invalid {ENV_WEBHOOK_URL}: {e}")

        # 2. Load from WECOM_BOTS JSON configuration
        bots_json = os.getenv(ENV_BOTS_CONFIG)
        if bots_json:
            try:
                bots_data = json.loads(bots_json)
                if isinstance(bots_data, dict):
                    for bot_id, bot_info in bots_data.items():
                        self._register_bot_from_dict(bot_id, bot_info)
                logger.debug(f"Loaded {len(bots_data)} bot(s) from {ENV_BOTS_CONFIG}")
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON in {ENV_BOTS_CONFIG}: {e}")

        # 3. Load from individual WECOM_BOT_<NAME>_URL variables
        for key, value in os.environ.items():
            match = ENV_BOT_URL_PATTERN.match(key)
            if match and value:
                bot_id = match.group(1).lower()
                if bot_id not in self._bots:
                    try:
                        self._bots[bot_id] = BotConfig(
                            name=bot_id,
                            webhook_url=value.strip(),
                            description=f"Bot from {key}",
                        )
                        logger.debug(f"Loaded bot '{bot_id}' from {key}")
                    except WeComError as e:
                        logger.warning(f"Invalid {key}: {e}")

    def _register_bot_from_dict(self, bot_id: str, bot_info: dict[str, Any] | str) -> None:
        """Register a bot from dictionary or string configuration.

        Args:
            bot_id: Unique identifier for the bot
            bot_info: Bot configuration (dict with name/webhook_url/description or just URL string)

        """
        bot_id = bot_id.lower()
        try:
            if isinstance(bot_info, str):
                # Simple format: {"bot_id": "webhook_url"}
                self._bots[bot_id] = BotConfig(
                    name=bot_id,
                    webhook_url=bot_info.strip(),
                )
            elif isinstance(bot_info, dict):
                # Full format: {"bot_id": {"name": "...", "webhook_url": "...", "description": "..."}}
                self._bots[bot_id] = BotConfig(
                    name=bot_info.get("name", bot_id),
                    webhook_url=bot_info.get("webhook_url", "").strip(),
                    description=bot_info.get("description", ""),
                    metadata=bot_info.get("metadata", {}),
                )
        except WeComError as e:
            logger.warning(f"Failed to register bot '{bot_id}': {e}")

    def register(self, bot_id: str, config: BotConfig) -> None:
        """Register a bot configuration.

        Args:
            bot_id: Unique identifier for the bot
            config: Bot configuration

        """
        self._ensure_loaded()
        self._bots[bot_id.lower()] = config
        logger.info(f"Registered bot '{bot_id}' ({config.name})")

    def get(self, bot_id: str | None = None) -> BotConfig:
        """Get a bot configuration by ID.

        Args:
            bot_id: Bot identifier. If None or empty, returns the default bot.

        Returns:
            BotConfig: The bot configuration

        Raises:
            WeComError: If bot is not found or no bots are configured

        """
        self._ensure_loaded()

        # Use default bot if no bot_id specified
        if not bot_id:
            bot_id = DEFAULT_BOT_NAME

        bot_id = bot_id.lower()

        if bot_id not in self._bots:
            available = list(self._bots.keys())
            if not available:
                raise WeComError(
                    "No bots configured. Set WECOM_WEBHOOK_URL or WECOM_BOTS environment variable.",
                    ErrorCode.VALIDATION_ERROR,
                )
            raise WeComError(
                f"Bot '{bot_id}' not found. Available bots: {', '.join(available)}",
                ErrorCode.VALIDATION_ERROR,
            )

        return self._bots[bot_id]

    def get_webhook_url(self, bot_id: str | None = None) -> str:
        """Get webhook URL for a bot.

        Args:
            bot_id: Bot identifier. If None, returns the default bot's URL.

        Returns:
            str: The webhook URL

        """
        return self.get(bot_id).webhook_url

    def list_bots(self) -> list[dict[str, str | bool]]:
        """List all configured bots.

        Returns:
            list: List of bot information dictionaries

        """
        self._ensure_loaded()
        return [
            {
                "id": bot_id,
                "name": config.name,
                "description": config.description,
                "has_webhook": bool(config.webhook_url),
            }
            for bot_id, config in self._bots.items()
        ]

    def has_bot(self, bot_id: str) -> bool:
        """Check if a bot is registered.

        Args:
            bot_id: Bot identifier

        Returns:
            bool: True if bot exists

        """
        self._ensure_loaded()
        return bot_id.lower() in self._bots

    def has_multiple_bots(self) -> bool:
        """Check if multiple bots are configured.

        Returns:
            bool: True if more than one bot is configured

        """
        self._ensure_loaded()
        return len(self._bots) > 1

    def get_bot_count(self) -> int:
        """Get the number of configured bots.

        Returns:
            int: Number of bots

        """
        self._ensure_loaded()
        return len(self._bots)

    def clear(self) -> None:
        """Clear all registered bots (mainly for testing)."""
        self._bots.clear()
        self._loaded = False

    def reload(self) -> None:
        """Reload bot configurations from environment."""
        self.clear()
        self._ensure_loaded()


# Global bot registry instance
_bot_registry: BotRegistry | None = None


def get_bot_registry() -> BotRegistry:
    """Get the global bot registry instance.

    Returns:
        BotRegistry: The global bot registry

    """
    global _bot_registry
    if _bot_registry is None:
        _bot_registry = BotRegistry()
    return _bot_registry


@lru_cache
def get_default_webhook_url() -> str:
    """Get the default webhook URL (backward compatible).

    This function maintains backward compatibility with code that expects
    a single webhook URL.

    Returns:
        str: The default webhook URL

    Raises:
        WeComError: If no default bot is configured

    """
    return get_bot_registry().get_webhook_url()


def get_webhook_url_for_bot(bot_id: str | None = None) -> str:
    """Get webhook URL for a specific bot.

    Args:
        bot_id: Bot identifier. If None, returns the default bot's URL.

    Returns:
        str: The webhook URL

    """
    return get_bot_registry().get_webhook_url(bot_id)


def list_available_bots() -> list[dict[str, str | bool]]:
    """List all available bots.

    Returns:
        list: List of bot information

    """
    return get_bot_registry().list_bots()


def get_multi_bot_instructions() -> str:
    """Get instructions for AI on how to use multiple bots.

    Returns:
        str: Instructions text for AI assistants

    """
    registry = get_bot_registry()
    bots = registry.list_bots()

    if not bots:
        return (
            "No WeCom bots are configured. Please set the WECOM_WEBHOOK_URL environment "
            "variable or configure multiple bots via WECOM_BOTS."
        )

    if len(bots) == 1:
        bot = bots[0]
        return (
            f"One WeCom bot is configured: '{bot['name']}' (id: {bot['id']}). "
            "All messages will be sent to this bot. You don't need to specify a bot_id."
        )

    # Multiple bots configured
    bot_list = "\n".join(
        f"  - **{bot['id']}**: {bot['name']}" + (f" - {bot['description']}" if bot["description"] else "")
        for bot in bots
    )

    return (
        f"## Multiple WeCom Bots Available\n\n"
        f"This server has {len(bots)} bots configured:\n{bot_list}\n\n"
        f"### How to Send Messages to Specific Bots\n"
        f"When calling `send_message`, `send_wecom_image`, or `send_wecom_file`, "
        f"you can specify the `bot_id` parameter to choose which bot to use:\n\n"
        f"- If `bot_id` is not specified, messages go to the **default** bot.\n"
        f"- To send to a specific bot, set `bot_id` to one of: {', '.join(b['id'] for b in bots)}\n\n"
        f"### Use Case Examples\n"
        f"- **Alert notifications**: Use the bot designated for alerts\n"
        f"- **CI/CD notifications**: Use the bot for build/deploy notifications\n"
        f"- **Team updates**: Use team-specific bots for targeted messaging\n\n"
        f"### Listing Bots\n"
        f"Call the `list_wecom_bots` tool to see all available bots and their configurations."
    )
