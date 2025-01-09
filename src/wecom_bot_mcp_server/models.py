"""Models for wecom_bot_mcp_server."""

# Import third-party modules
from pydantic import (
    BaseModel,  # type: ignore
    Field,
)

# Import local modules
from wecom_bot_mcp_server.text_utils import fix_encoding


class Message(BaseModel):  # type: ignore
    """Message model for WeCom bot."""

    content: str = Field(description="Message content to send", min_length=1)
    msgtype: str = Field(default="markdown", description="Message type", pattern="^(text|markdown|news|file|image)$")

    @classmethod
    def model_validate(cls, *args, **kwargs):
        """Validate and fix encoding of the message content."""
        obj = super().model_validate(*args, **kwargs)
        if isinstance(obj, cls):
            obj.content = fix_encoding(obj.content)
        return obj


class MessageHistory(BaseModel):  # type: ignore
    """Message history model."""

    role: str = Field(description="Role of the message sender")
    content: str = Field(description="Message content")
    status: str = Field(description="Message status")
    timestamp: str = Field(description="Message timestamp")
