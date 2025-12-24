# 消息类型

WeCom Bot MCP Server 支持多种消息类型，满足各种通信需求。

## 文本消息

用于简单通知的基本文本消息。

```python
await send_message(
    content="你好，世界！",
    msg_type="text"
)
```

### 带 @提及

通过用户 ID 提及特定用户：

```python
await send_message(
    content="你好 @user1 @user2，请查看这个",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)
```

通过手机号提及用户：

```python
await send_message(
    content="紧急：请回复",
    msg_type="text",
    mentioned_mobile_list=["13800138000", "13900139000"]
)
```

提及所有成员：

```python
await send_message(
    content="重要公告",
    msg_type="text",
    mentioned_list=["@all"]
)
```

## Markdown 消息

支持 Markdown 格式的富文本消息。

```python
await send_message(
    content="""# 项目更新

## 状态
- **后端**：✅ 完成
- **前端**：🔄 进行中
- **测试**：⏳ 待开始

> 下一个里程碑：12月30日
""",
    msg_type="markdown"
)
```

### 支持的 Markdown 语法

| 语法 | 描述 |
|------|------|
| `# 标题` | 1-6 级标题 |
| `**粗体**` | 粗体文本 |
| `*斜体*` | 斜体文本 |
| `[链接](url)` | 超链接 |
| `> 引用` | 块引用 |
| `- 项目` | 无序列表 |
| `1. 项目` | 有序列表 |
| `` `代码` `` | 行内代码 |
| `<font color="red">文本</font>` | 彩色文本 |

::: tip
Markdown 消息不支持 @提及。如需提及用户，请使用文本消息。
:::

## 图片消息

从本地文件或 URL 发送图片。

### 从本地文件

```python
await send_wecom_image("/path/to/image.png")
```

### 从 URL

```python
await send_wecom_image("https://example.com/image.png")
```

### 支持的格式

- PNG（推荐）
- JPG/JPEG
- GIF（仅静态）

::: warning 大小限制
图片必须小于 2MB。超大图片将自动压缩。
:::

## 文件消息

发送任何类型的文件到群组。

```python
await send_wecom_file("/path/to/document.pdf")
```

### 支持的文件类型

支持所有文件类型，包括：
- 文档：PDF、Word、Excel、PowerPoint
- 压缩包：ZIP、RAR、7z
- 代码文件：.py、.js、.json 等
- 更多...

::: warning 大小限制
文件必须小于 20MB。
:::

## 消息类型对比

| 功能 | 文本 | Markdown | 图片 | 文件 |
|------|------|----------|------|------|
| 富文本格式 | ❌ | ✅ | N/A | N/A |
| @提及 | ✅ | ❌ | ❌ | ❌ |
| 超链接 | ❌ | ✅ | N/A | N/A |
| 附件 | ❌ | ❌ | ✅ | ✅ |
| 最大大小 | N/A | N/A | 2MB | 20MB |

## 最佳实践

1. **使用 Markdown** 发送格式化报告和公告
2. **使用文本** 当需要 @提及用户时
3. **压缩图片** 发送前减小文件大小
4. **使用描述性文件名** 发送文件时
