# 快速开始

WeCom Bot MCP Server 是一个遵循 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的服务器，使 AI 助手能够向企业微信群组发送消息。

## 什么是 MCP？

Model Context Protocol (MCP) 是一个开放标准，允许 AI 助手与外部工具和服务交互。通过实现 MCP，此服务器使 Claude 等 AI 助手能够向企业微信群组发送消息、文件和图片。

## 功能特点

- **多种消息类型**：发送文本、Markdown、图片和文件
- **@提及支持**：通过用户 ID 或手机号提及用户
- **多机器人支持**：配置和使用多个企业微信机器人
- **跨平台**：支持 Windows、macOS 和 Linux
- **MCP 兼容**：支持 Claude Desktop、Cline、Windsurf 等

## 前置条件

开始之前，请确保：

1. 安装了 **Python 3.10+**
2. 从企业微信群组设置中获取 **机器人 Webhook URL**

### 获取 Webhook URL

1. 打开企业微信群组
2. 点击群组设置（右上角三个点）
3. 选择"群机器人"
4. 点击"添加机器人"或选择现有机器人
5. 复制 Webhook URL

::: warning 安全提示
请妥善保管您的 webhook URL。任何拥有此 URL 的人都可以向您的群组发送消息。
:::

## 下一步

- [安装指南](./installation) - 详细安装说明
- [快速上手](./quick-start) - 发送您的第一条消息
- [配置](../config/) - 配置环境变量和 MCP 客户端
