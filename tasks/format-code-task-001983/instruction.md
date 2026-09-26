## Duplicate permissions shown in WebExtension permissions list

When viewing an add-on whose `manifest.json` happens to repeat the same WebExtension permission (or whose `content_scripts` `matches` overlap with a host permission already declared in the top-level `permissions` array), the duplicates are not collapsed — the same permission ends up listed twice (or more) in the displayed permissions list.

For example, an add-on with a manifest along the lines of:

```json
{
  "permissions": [
    "tabs",
    "https://example.com/*",
    "tabs"
  ],
  "content_scripts": [
    {
      "matches": ["https://example.com/*"],
      "js": ["content.js"]
    }
  ]
}
```

ends up surfacing `"tabs"` twice and `"https://example.com/*"` twice. The user-visible permissions list should report each permission only once, while otherwise preserving the order in which they appear.
