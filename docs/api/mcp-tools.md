# MCP Tools Reference

These tools are available to AI assistants when using WeCom Bot MCP Server.

## send_message

Send text or markdown messages to WeCom.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `content` | string | Yes | Message content |
| `msg_type` | string | No | Message type: `text` (default) or `markdown` |
| `mentioned_list` | array | No | List of user IDs to @mention |
| `mentioned_mobile_list` | array | No | List of phone numbers to @mention |
| `bot_id` | string | No | Target bot ID (uses default if not specified) |

### Examples

**Simple text message:**
```
Send "Hello team!" to WeCom
```

**Markdown message:**
```
Send a markdown message to WeCom with the build status
```

**With @mentions:**
```
Send a reminder to WeCom and mention user1 and user2
```

**To specific bot:**
```
Send an alert to the alert bot: Server is down!
```

### Response

```json
{
  "status": "success",
  "message": "Message sent successfully",
  "bot_id": "default"
}
```

## send_wecom_file

Send a file to WeCom.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | string | Yes | Path to the file |
| `bot_id` | string | No | Target bot ID |

### Examples

**Send a file:**
```
Send the file /path/to/report.pdf to WeCom
```

**Send to specific bot:**
```
Send the build log to the CI bot
```

### Response

```json
{
  "status": "success",
  "message": "File sent successfully",
  "file_info": {
    "name": "report.pdf",
    "size": 1024
  }
}
```

### Limitations

- Maximum file size: 20MB
- All file types are supported

## send_wecom_image

Send an image to WeCom.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_path` | string | Yes | Path to image file or URL |
| `bot_id` | string | No | Target bot ID |

### Examples

**Send local image:**
```
Send the image /path/to/chart.png to WeCom
```

**Send from URL:**
```
Send this image to WeCom: https://example.com/image.png
```

### Response

```json
{
  "status": "success",
  "message": "Image sent successfully",
  "image_info": {
    "format": "png",
    "size": 2048
  }
}
```

### Limitations

- Maximum size: 2MB
- Supported formats: PNG, JPG, JPEG, GIF (static)
- Images exceeding size limit are automatically compressed

## list_wecom_bots

List all configured WeCom bots.

### Parameters

None

### Examples

```
What WeCom bots are available?
```

```
List all configured bots
```

### Response

```json
{
  "bots": [
    {
      "id": "default",
      "name": "Default Bot",
      "description": "Default bot (from WECOM_WEBHOOK_URL)",
      "has_webhook": true
    },
    {
      "id": "alert",
      "name": "Alert Bot",
      "description": "For system alerts",
      "has_webhook": true
    }
  ],
  "count": 2
}
```

## Error Handling

All tools return errors in a consistent format:

```json
{
  "status": "error",
  "error": "Error message",
  "error_code": "VALIDATION_ERROR"
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Invalid parameters |
| `NETWORK_ERROR` | Network connection failed |
| `API_ERROR` | WeCom API returned an error |
| `FILE_NOT_FOUND` | File does not exist |
| `FILE_TOO_LARGE` | File exceeds size limit |

## Usage Tips for AI Assistants

1. **Default bot**: If the user doesn't specify a bot, use the default bot
2. **Bot selection**: Use `list_wecom_bots` to find available bots when needed
3. **Message type**: Use `markdown` for formatted content, `text` for simple messages with @mentions
4. **File paths**: Accept both absolute and relative paths
5. **Error recovery**: If a bot is not found, list available bots and ask the user to choose
