# 工具注册系统更新

在 README.md 文件的 "Development" 部分之前添加以下内容：

## 扩展功能

### 工具注册系统

WeCom Bot MCP Server 提供了一个灵活的工具注册系统，使开发者能够轻松地添加自定义工具。

#### 使用装饰器注册工具

```python
from wecom_bot_mcp_server.tools import register_tool

@register_tool(category="custom", description="Send custom notification")
async def send_notification(title: str, content: str, ctx=None):
    message = f"# {title}\n\n{content}"
    return await send_message(content=message, msg_type="markdown", ctx=ctx)
```

#### 查询可用工具

```python
from wecom_bot_mcp_server.tools import tools

# List all tools
all_tools = tools.list_tools()

# List tools by category
message_tools = tools.list_tools(category="message")
```

#### 自定义服务器示例

```python
# Import custom tools
import my_custom_tools

# Start the server with custom tools
from wecom_bot_mcp_server.server import main

if __name__ == "__main__":
    main()
```

详细文档请参阅 [工具注册系统](docs/tools_registry.md)。
