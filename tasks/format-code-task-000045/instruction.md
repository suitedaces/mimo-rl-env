Add support for content_type: "location" and "image_url" on Quick Replies
We need to refactor the `_formatQuickReplies` method to support an object with an open format. New types of quick replies format added since we implemented this methods are:

Location:

```
    {
        "content_type":"location",
    }
```

Text with Image:

```
    {
        "content_type":"text",
        "title":"Green",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN",
        "image_url":"http://petersfantastichats.com/img/green.png"
    }
```

But more formats will likely be added in the future so we should support whatever object the user sends (or auto-format like we do now if it's a string).

Facebook Docs: https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies
