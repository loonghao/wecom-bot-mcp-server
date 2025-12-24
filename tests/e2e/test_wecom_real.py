"""Real E2E tests for WeCom Bot MCP Server.

These tests send actual messages to a real WeCom webhook.
They are only run when WECOM_WEBHOOK_URL environment variable is set.

To run these tests locally:
    export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    pytest tests/e2e/test_wecom_real.py -v -m e2e_real

In CI, configure WECOM_WEBHOOK_URL as a secret environment variable.
"""

# Import built-in modules
from datetime import datetime
import os

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.message import send_message


def get_webhook_url() -> str:
    """Get the webhook URL from environment variable."""
    return os.environ.get("WECOM_WEBHOOK_URL", "").strip()


def is_real_e2e_enabled() -> bool:
    """Check if real E2E tests should run.

    Returns True only if WECOM_WEBHOOK_URL is set and contains a valid URL.
    """
    url = get_webhook_url()
    return bool(url) and url.startswith("https://qyapi.weixin.qq.com/")


@pytest.mark.e2e_real
@pytest.mark.skipif(not is_real_e2e_enabled(), reason="WECOM_WEBHOOK_URL not set")
@pytest.mark.asyncio
async def test_send_message_mention_all():
    """Test sending a message that mentions @all."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# E2E Test - @all Mention

**Test Time**: {timestamp}

<@all> This is an E2E test message from wecom-bot-mcp-server.

Test completed successfully!
"""

    result = await send_message(
        content=content,
        msg_type="markdown",
        mentioned_list=["@all"],
    )

    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"
