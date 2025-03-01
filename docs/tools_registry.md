# 工具注册系统

WeCom Bot MCP Server 提供了一个灵活的工具注册系统，使开发者能够轻松地添加自定义工具。

## 基本用法

### 使用装饰器注册工具

最简单的方式是使用 `@register_tool` 装饰器：

```python
from wecom_bot_mcp_server.tools import register_tool

@register_tool(category="custom", description="发送自定义消息")
async def send_custom_message(content: str, ctx=None):
    # 实现自定义消息发送逻辑
    pass
```

### 装饰器参数

`@register_tool` 装饰器接受以下参数：

- `name`：工具名称（默认为函数名）
- `category`：工具类别（用于分组和查询）
- `description`：工具描述（默认使用函数文档字符串的第一段）

### 手动注册工具

也可以直接使用 `ToolRegistry` 实例手动注册工具：

```python
from wecom_bot_mcp_server.tools import tools

async def my_custom_tool(param1, param2, ctx=None):
    # 实现自定义工具逻辑
    pass

tools.add_tool(
    name="my_custom_tool",
    func=my_custom_tool,
    category="custom",
    description="自定义工具示例"
)
```

## 工具分类

工具可以按类别分组，便于管理和查询：

- `message`：消息相关工具
- `file`：文件相关工具
- `image`：图片相关工具
- `custom`：自定义工具

## 查询工具

可以通过以下方式查询已注册的工具：

```python
from wecom_bot_mcp_server.tools import tools

# 列出所有工具
all_tools = tools.list_tools()

# 列出特定类别的工具
message_tools = tools.list_tools(category="message")

# 列出所有类别
categories = tools.list_categories()

# 获取特定工具的信息
tool_info = tools.get_tool("send_message")

# 获取特定工具的函数
tool_func = tools.get_function("send_message")
```

## 示例：添加自定义工具

以下是添加自定义工具的完整示例：

```python
# custom_tools.py
from wecom_bot_mcp_server.tools import register_tool
from wecom_bot_mcp_server.message import send_message

@register_tool(category="custom", description="发送问候消息")
async def send_greeting(name: str, ctx=None):
    """发送问候消息到企业微信。
    
    Args:
        name: 要问候的名称
        ctx: FastMCP 上下文
    """
    greeting = f"# 你好，{name}！\n\n欢迎使用 WeCom Bot MCP Server！"
    return await send_message(content=greeting, msg_type="markdown", ctx=ctx)
```

然后在应用程序中导入此模块：

```python
# 导入自定义工具
import custom_tools

# 启动服务器
from wecom_bot_mcp_server.server import main

if __name__ == "__main__":
    main()
```

## 工具注册流程

1. 工具通过装饰器或手动方法注册到 `ToolRegistry` 实例
2. 服务器启动时，`tools.register_with_mcp(mcp)` 将所有注册的工具添加到 MCP 服务器
3. 工具可以通过 MCP 协议调用

## 最佳实践

- 为每个工具提供清晰的文档字符串
- 使用有意义的类别组织工具
- 保持工具功能单一，遵循单一职责原则
- 处理异常并提供有用的错误消息
- 使用类型提示增强代码可读性和工具支持
