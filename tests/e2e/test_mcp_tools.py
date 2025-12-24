"""E2E tests for MCP tools using in-memory transport.

These tests verify that the MCP server tools work correctly through
the MCP protocol, using an in-memory client-server connection.

Note: These tests focus on MCP protocol correctness, not actual message sending.
For actual message sending tests, see test_wecom_real.py.
"""

# Import third-party modules
import pytest
from mcp.client.session import ClientSession
from mcp.types import TextContent


@pytest.mark.anyio
@pytest.mark.e2e
async def test_list_tools(client_session: ClientSession):
    """Test that all expected tools are available via MCP protocol."""
    tools = await client_session.list_tools()
    tool_names = [tool.name for tool in tools.tools]

    # Verify expected tools are present
    assert "send_message" in tool_names
    assert "send_wecom_file" in tool_names
    assert "send_wecom_image" in tool_names
    assert "send_wecom_template_card_text_notice" in tool_names
    assert "send_wecom_template_card_news_notice" in tool_names


@pytest.mark.anyio
@pytest.mark.e2e
async def test_send_message_tool_schema(client_session: ClientSession):
    """Test send_message tool has correct schema."""
    tools = await client_session.list_tools()
    send_message_tool = next((t for t in tools.tools if t.name == "send_message"), None)

    assert send_message_tool is not None
    assert send_message_tool.inputSchema is not None

    # Verify msg_type parameter description contains guidance
    schema = send_message_tool.inputSchema
    properties = schema.get("properties", {})
    msg_type_prop = properties.get("msg_type", {})

    # Check that the description contains guidance for choosing msg_type
    description = msg_type_prop.get("description", "")
    assert "markdown" in description.lower()
    assert "markdown_v2" in description.lower()


@pytest.mark.anyio
@pytest.mark.e2e
async def test_send_message_tool_schema_has_enum(client_session: ClientSession):
    """Test send_message tool msg_type has correct enum values."""
    tools = await client_session.list_tools()
    send_message_tool = next((t for t in tools.tools if t.name == "send_message"), None)

    assert send_message_tool is not None
    schema = send_message_tool.inputSchema
    properties = schema.get("properties", {})
    msg_type_prop = properties.get("msg_type", {})

    # Check that enum contains both markdown types
    enum_values = msg_type_prop.get("enum", [])
    assert "markdown" in enum_values
    assert "markdown_v2" in enum_values


@pytest.mark.anyio
@pytest.mark.e2e
async def test_list_prompts(client_session: ClientSession):
    """Test that prompts are available via MCP protocol."""
    prompts = await client_session.list_prompts()
    prompt_names = [p.name for p in prompts.prompts]

    # Verify the message guidelines prompt is present
    assert "wecom_message_guidelines" in prompt_names


@pytest.mark.anyio
@pytest.mark.e2e
async def test_get_prompt_content(client_session: ClientSession):
    """Test getting prompt content via MCP protocol."""
    result = await client_session.get_prompt("wecom_message_guidelines")

    # Verify prompt contains guidance
    assert result.messages is not None
    assert len(result.messages) > 0

    # Get the text content from the prompt
    content = result.messages[0].content
    if isinstance(content, TextContent):
        text = content.text
    else:
        text = str(content)

    # Verify key guidance is present
    assert "markdown" in text.lower()
    assert "markdown_v2" in text.lower()


@pytest.mark.anyio
@pytest.mark.e2e
async def test_list_resources(client_session: ClientSession):
    """Test that resources are available via MCP protocol."""
    resources = await client_session.list_resources()
    resource_uris = [r.uri for r in resources.resources]

    # Verify expected resources are present
    assert any("markdown-capabilities" in str(uri) for uri in resource_uris)
    assert any("messages" in str(uri) for uri in resource_uris)


@pytest.mark.anyio
@pytest.mark.e2e
async def test_read_markdown_capabilities_resource(client_session: ClientSession):
    """Test reading markdown capabilities resource via MCP protocol."""
    result = await client_session.read_resource("wecom://markdown-capabilities")

    # Verify resource content
    assert result.contents is not None
    assert len(result.contents) > 0

    # Get text content
    content = result.contents[0]
    text = content.text if hasattr(content, "text") else str(content)

    # Verify key information is present
    assert "markdown" in text.lower()
    assert "markdown_v2" in text.lower()
    assert "<@userid>" in text or "@userid" in text.lower()


@pytest.mark.anyio
@pytest.mark.e2e
async def test_call_send_message_tool_invalid_type(client_session: ClientSession):
    """Test that send_message tool rejects invalid msg_type."""
    # Call the tool with invalid msg_type - should raise an error
    result = await client_session.call_tool(
        "send_message",
        {
            "content": "Test message",
            "msg_type": "invalid_type",
        },
    )

    # The tool should return an error
    assert result is not None
    # Check if there's an error in the result
    content_text = str(result.content[0]) if result.content else ""
    assert "error" in content_text.lower() or result.isError


@pytest.mark.anyio
@pytest.mark.e2e
async def test_call_send_message_tool_missing_content(client_session: ClientSession):
    """Test that send_message tool requires content parameter."""
    # Call the tool without content - should raise an error
    result = await client_session.call_tool(
        "send_message",
        {
            "msg_type": "markdown_v2",
        },
    )

    # The tool should return an error
    assert result is not None
    content_text = str(result.content[0]) if result.content else ""
    # Either isError is True or the content contains an error message
    assert result.isError or "error" in content_text.lower() or "content" in content_text.lower()


@pytest.mark.anyio
@pytest.mark.e2e
async def test_template_card_tool_schema(client_session: ClientSession):
    """Test template card tools have correct schema."""
    tools = await client_session.list_tools()

    # Check text_notice template card
    text_notice_tool = next((t for t in tools.tools if t.name == "send_wecom_template_card_text_notice"), None)
    assert text_notice_tool is not None
    assert text_notice_tool.inputSchema is not None

    # Check news_notice template card
    news_notice_tool = next((t for t in tools.tools if t.name == "send_wecom_template_card_news_notice"), None)
    assert news_notice_tool is not None
    assert news_notice_tool.inputSchema is not None


@pytest.mark.anyio
@pytest.mark.e2e
async def test_file_tool_schema(client_session: ClientSession):
    """Test file upload tool has correct schema."""
    tools = await client_session.list_tools()
    file_tool = next((t for t in tools.tools if t.name == "send_wecom_file"), None)

    assert file_tool is not None
    assert file_tool.inputSchema is not None

    # Verify required parameter
    schema = file_tool.inputSchema
    required = schema.get("required", [])
    assert "file_path" in required


@pytest.mark.anyio
@pytest.mark.e2e
async def test_image_tool_schema(client_session: ClientSession):
    """Test image upload tool has correct schema."""
    tools = await client_session.list_tools()
    image_tool = next((t for t in tools.tools if t.name == "send_wecom_image"), None)

    assert image_tool is not None
    assert image_tool.inputSchema is not None

    # Verify required parameter
    schema = image_tool.inputSchema
    required = schema.get("required", [])
    assert "image_path" in required


@pytest.mark.anyio
@pytest.mark.e2e
async def test_prompt_description_contains_usage_guide(client_session: ClientSession):
    """Test that prompt description contains usage guidance."""
    prompts = await client_session.list_prompts()
    guidelines_prompt = next((p for p in prompts.prompts if p.name == "wecom_message_guidelines"), None)

    assert guidelines_prompt is not None
    assert guidelines_prompt.description is not None
    # Description should mention what the prompt is for
    assert len(guidelines_prompt.description) > 0
