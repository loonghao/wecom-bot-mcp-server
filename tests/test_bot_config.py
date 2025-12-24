"""Tests for multi-bot configuration module."""

# Import built-in modules
import json
import os

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.bot_config import BotConfig
from wecom_bot_mcp_server.bot_config import BotRegistry
from wecom_bot_mcp_server.errors import WeComError


class TestBotConfig:
    """Tests for BotConfig dataclass."""

    def test_valid_bot_config(self):
        """Test creating a valid bot configuration."""
        config = BotConfig(
            name="Test Bot",
            webhook_url="https://example.com/webhook",
            description="A test bot",
        )
        assert config.name == "Test Bot"
        assert config.webhook_url == "https://example.com/webhook"
        assert config.description == "A test bot"

    def test_bot_config_with_http(self):
        """Test bot config with http URL."""
        config = BotConfig(
            name="HTTP Bot",
            webhook_url="http://example.com/webhook",
        )
        assert config.webhook_url == "http://example.com/webhook"

    def test_bot_config_empty_url_raises_error(self):
        """Test that empty webhook URL raises error."""
        with pytest.raises(WeComError) as exc_info:
            BotConfig(name="Test", webhook_url="")
        assert "empty webhook_url" in str(exc_info.value)

    def test_bot_config_invalid_url_raises_error(self):
        """Test that invalid URL protocol raises error."""
        with pytest.raises(WeComError) as exc_info:
            BotConfig(name="Test", webhook_url="ftp://example.com")
        assert "must start with" in str(exc_info.value)


class TestBotRegistry:
    """Tests for BotRegistry class."""

    @pytest.fixture
    def clean_env(self):
        """Fixture to clean environment variables."""
        env_vars = [
            "WECOM_WEBHOOK_URL",
            "WECOM_BOTS",
            "WECOM_BOT_ALERT_URL",
            "WECOM_BOT_CI_URL",
        ]
        original = {k: os.environ.get(k) for k in env_vars}
        for k in env_vars:
            if k in os.environ:
                del os.environ[k]
        yield
        # Restore original values
        for k, v in original.items():
            if v is not None:
                os.environ[k] = v
            elif k in os.environ:
                del os.environ[k]

    def test_load_default_bot_from_env(self, clean_env):
        """Test loading default bot from WECOM_WEBHOOK_URL."""
        os.environ["WECOM_WEBHOOK_URL"] = "https://example.com/default"
        registry = BotRegistry()
        registry.reload()

        assert registry.has_bot("default")
        assert registry.get_webhook_url() == "https://example.com/default"
        assert registry.get_webhook_url("default") == "https://example.com/default"

    def test_load_bots_from_json(self, clean_env):
        """Test loading bots from WECOM_BOTS JSON."""
        bots_config = {
            "alert": {
                "name": "Alert Bot",
                "webhook_url": "https://example.com/alert",
                "description": "For alerts",
            },
            "ci": "https://example.com/ci",  # Simple format
        }
        os.environ["WECOM_BOTS"] = json.dumps(bots_config)
        registry = BotRegistry()
        registry.reload()

        assert registry.has_bot("alert")
        assert registry.has_bot("ci")
        assert registry.get_webhook_url("alert") == "https://example.com/alert"
        assert registry.get_webhook_url("ci") == "https://example.com/ci"

    def test_load_bots_from_individual_env_vars(self, clean_env):
        """Test loading bots from WECOM_BOT_<NAME>_URL variables."""
        os.environ["WECOM_BOT_ALERT_URL"] = "https://example.com/alert"
        os.environ["WECOM_BOT_CI_URL"] = "https://example.com/ci"
        registry = BotRegistry()
        registry.reload()

        assert registry.has_bot("alert")
        assert registry.has_bot("ci")
        assert registry.get_webhook_url("alert") == "https://example.com/alert"
        assert registry.get_webhook_url("ci") == "https://example.com/ci"

    def test_combined_configuration(self, clean_env):
        """Test combining multiple configuration methods."""
        os.environ["WECOM_WEBHOOK_URL"] = "https://example.com/default"
        os.environ["WECOM_BOT_ALERT_URL"] = "https://example.com/alert"
        registry = BotRegistry()
        registry.reload()

        assert registry.has_bot("default")
        assert registry.has_bot("alert")
        assert registry.has_multiple_bots()
        assert registry.get_bot_count() == 2

    def test_get_nonexistent_bot_raises_error(self, clean_env):
        """Test that getting nonexistent bot raises error."""
        os.environ["WECOM_WEBHOOK_URL"] = "https://example.com/default"
        registry = BotRegistry()
        registry.reload()

        with pytest.raises(WeComError) as exc_info:
            registry.get("nonexistent")
        assert "not found" in str(exc_info.value)

    def test_no_bots_configured_raises_error(self, clean_env):
        """Test that no bots configured raises error."""
        registry = BotRegistry()
        registry.reload()

        with pytest.raises(WeComError) as exc_info:
            registry.get()
        assert "No bots configured" in str(exc_info.value)

    def test_list_bots(self, clean_env):
        """Test listing all bots."""
        os.environ["WECOM_WEBHOOK_URL"] = "https://example.com/default"
        os.environ["WECOM_BOT_ALERT_URL"] = "https://example.com/alert"
        registry = BotRegistry()
        registry.reload()

        bots = registry.list_bots()
        assert len(bots) == 2
        bot_ids = [b["id"] for b in bots]
        assert "default" in bot_ids
        assert "alert" in bot_ids

    def test_register_bot_programmatically(self, clean_env):
        """Test registering a bot programmatically."""
        registry = BotRegistry()
        registry.reload()

        config = BotConfig(
            name="Custom Bot",
            webhook_url="https://example.com/custom",
        )
        registry.register("custom", config)

        assert registry.has_bot("custom")
        assert registry.get_webhook_url("custom") == "https://example.com/custom"

    def test_bot_id_case_insensitive(self, clean_env):
        """Test that bot IDs are case insensitive."""
        os.environ["WECOM_BOT_ALERT_URL"] = "https://example.com/alert"
        registry = BotRegistry()
        registry.reload()

        assert registry.has_bot("alert")
        assert registry.has_bot("ALERT")
        assert registry.has_bot("Alert")
        assert registry.get_webhook_url("ALERT") == "https://example.com/alert"


class TestMultiBotInstructions:
    """Tests for multi-bot instruction generation."""

    @pytest.fixture(autouse=True)
    def clean_env(self):
        """Clean environment variables for these tests."""
        # Import here to avoid circular imports
        # Import local modules
        import wecom_bot_mcp_server.bot_config as bot_config

        # Save and remove all WeCom-related env vars
        saved_env = {}
        keys_to_remove = [k for k in os.environ if k.startswith("WECOM_")]
        for key in keys_to_remove:
            saved_env[key] = os.environ.pop(key)

        # Reset registry to ensure clean state
        bot_config._bot_registry = None

        yield

        # Restore env vars
        os.environ.update(saved_env)
        # Reset registry again after test
        bot_config._bot_registry = None

    def test_no_bots_instructions(self):
        """Test instructions when no bots configured."""
        # Import fresh to ensure we use the reset registry
        # Import local modules
        import wecom_bot_mcp_server.bot_config as bot_config

        # Ensure registry is None before test
        bot_config._bot_registry = None

        # With clean environment, registry should have no bots
        instructions = bot_config.get_multi_bot_instructions()
        assert "No WeCom bots are configured" in instructions

    def test_single_bot_instructions(self):
        """Test instructions with single bot."""
        # Import local modules
        import wecom_bot_mcp_server.bot_config as bot_config

        # Set up single bot via environment
        os.environ["WECOM_WEBHOOK_URL"] = "https://example.com/default"
        # Reset registry to pick up new env var
        bot_config._bot_registry = None

        instructions = bot_config.get_multi_bot_instructions()
        assert "One WeCom bot is configured" in instructions

    def test_multiple_bots_instructions(self):
        """Test instructions with multiple bots."""
        # Import local modules
        import wecom_bot_mcp_server.bot_config as bot_config

        # Set up multiple bots via environment
        os.environ["WECOM_BOTS"] = json.dumps(
            {
                "default": {
                    "name": "default",
                    "webhook_url": "https://example.com/default",
                    "description": "Default bot",
                },
                "alert": {
                    "name": "alert",
                    "webhook_url": "https://example.com/alert",
                    "description": "Alert bot",
                },
            }
        )
        # Reset registry to pick up new env var
        bot_config._bot_registry = None

        instructions = bot_config.get_multi_bot_instructions()
        assert "Multiple WeCom Bots Available" in instructions
        assert "bot_id" in instructions


class TestListAvailableBots:
    """Tests for list_available_bots function."""

    @pytest.fixture(autouse=True)
    def clean_env(self):
        """Clean environment variables for these tests."""
        # Import local modules
        import wecom_bot_mcp_server.bot_config as bot_config

        # Save and remove all WeCom-related env vars
        saved_env = {}
        keys_to_remove = [k for k in os.environ if k.startswith("WECOM_")]
        for key in keys_to_remove:
            saved_env[key] = os.environ.pop(key)

        # Reset registry to ensure clean state
        bot_config._bot_registry = None

        yield

        # Restore env vars
        os.environ.update(saved_env)
        # Reset registry again after test
        bot_config._bot_registry = None

    def test_list_available_bots(self):
        """Test listing available bots."""
        # Import local modules
        import wecom_bot_mcp_server.bot_config as bot_config

        # Set up multiple bots via environment
        os.environ["WECOM_BOTS"] = json.dumps(
            {
                "default": {
                    "name": "default",
                    "webhook_url": "https://example.com/default",
                    "description": "Default bot",
                },
                "alert": {
                    "name": "alert",
                    "webhook_url": "https://example.com/alert",
                    "description": "Alert bot",
                },
            }
        )
        # Reset registry to pick up new env var
        bot_config._bot_registry = None

        bots = bot_config.list_available_bots()
        assert len(bots) == 2
        assert any(b["id"] == "default" for b in bots)
        assert any(b["id"] == "alert" for b in bots)
