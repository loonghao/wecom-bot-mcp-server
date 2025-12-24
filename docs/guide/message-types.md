# Message Types

WeCom Bot MCP Server supports multiple message types to meet various communication needs.

## Text Messages

Basic text messages for simple notifications.

```python
await send_message(
    content="Hello, World!",
    msg_type="text"
)
```

### With @Mentions

Mention specific users by their user ID:

```python
await send_message(
    content="Hello @user1 @user2, please check this",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)
```

Mention users by phone number:

```python
await send_message(
    content="Urgent: Please respond",
    msg_type="text",
    mentioned_mobile_list=["13800138000", "13900139000"]
)
```

Mention all members:

```python
await send_message(
    content="Important announcement for everyone",
    msg_type="text",
    mentioned_list=["@all"]
)
```

## Markdown Messages

Rich formatted messages with markdown support.

```python
await send_message(
    content="""# Project Update

## Status
- **Backend**: ✅ Complete
- **Frontend**: 🔄 In Progress
- **Testing**: ⏳ Pending

> Next milestone: December 30th
""",
    msg_type="markdown"
)
```

### Supported Markdown Syntax

| Syntax | Description |
|--------|-------------|
| `# Heading` | Heading levels 1-6 |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `[link](url)` | Hyperlinks |
| `> quote` | Block quotes |
| `- item` | Unordered lists |
| `1. item` | Ordered lists |
| `` `code` `` | Inline code |
| `<font color="red">text</font>` | Colored text |

::: tip
Markdown messages don't support @mentions. Use text messages if you need to mention users.
:::

## Image Messages

Send images from local files or URLs.

### From Local File

```python
await send_wecom_image("/path/to/image.png")
```

### From URL

```python
await send_wecom_image("https://example.com/image.png")
```

### Supported Formats

- PNG (recommended)
- JPG/JPEG
- GIF (static only)

::: warning Size Limit
Images must be under 2MB. Larger images will be automatically compressed.
:::

## File Messages

Send any file type to the group.

```python
await send_wecom_file("/path/to/document.pdf")
```

### Supported File Types

All file types are supported, including:
- Documents: PDF, Word, Excel, PowerPoint
- Archives: ZIP, RAR, 7z
- Code files: .py, .js, .json, etc.
- And more...

::: warning Size Limit
Files must be under 20MB.
:::

## Message Type Comparison

| Feature | Text | Markdown | Image | File |
|---------|------|----------|-------|------|
| Rich formatting | ❌ | ✅ | N/A | N/A |
| @Mentions | ✅ | ❌ | ❌ | ❌ |
| Hyperlinks | ❌ | ✅ | N/A | N/A |
| File attachment | ❌ | ❌ | ✅ | ✅ |
| Max size | N/A | N/A | 2MB | 20MB |

## Best Practices

1. **Use Markdown** for formatted reports and announcements
2. **Use Text** when you need to @mention users
3. **Compress images** before sending to reduce upload time
4. **Use descriptive filenames** for file messages
