# 安装

根据您的使用场景，有多种方式安装 WeCom Bot MCP Server。

## 自动安装（推荐）

### 使用 Smithery

对于 Claude Desktop 用户，Smithery 提供最简单的安装方式：

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

### 使用 Cline 插件

1. 从 VSCode 市场安装 [Cline 插件](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. 打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）
3. 搜索 "Cline: Install Package"
4. 输入 "wecom-bot-mcp-server" 并按回车

## 手动安装

### 使用 pip

```bash
pip install wecom-bot-mcp-server
```

### 使用 uv（推荐 Python 用户）

```bash
# 如果尚未安装 uv
pip install uv

# 直接运行，无需安装
uvx wecom-bot-mcp-server
```

### 使用 pipx

```bash
pipx install wecom-bot-mcp-server
```

## Docker 安装

```bash
docker pull loonghao/wecom-bot-mcp-server

docker run -e WECOM_WEBHOOK_URL="your-webhook-url" loonghao/wecom-bot-mcp-server
```

## 验证安装

安装后，验证是否正常工作：

```bash
# 检查版本
wecom-bot-mcp-server --version

# 或使用 uvx
uvx wecom-bot-mcp-server --version
```

## 下一步

- [快速上手](./quick-start) - 配置并发送第一条消息
- [MCP 客户端配置](../config/mcp-clients) - 设置您的 AI 助手
