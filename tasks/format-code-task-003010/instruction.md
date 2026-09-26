### Describe the bug

dev mode for firefox mv2 failed to copy host_permissions to permissions.
Errors example,

<span style="color: red;">
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at http://110.42.229.221:8080/search/word/search. (Reason: CORS header ‘Access-Control-Allow-Origin’ missing). Status code: 403.
</span>


### To Reproduce

Use when `pnpm dev -b firefox` to launch firefox mv2,  the `<rootDir>/.output/firefox-mv2/manifest.json` missed out important `host_permissions` defined in `wxt.config.ts`


Steps to reproduce the bug using the reproduction:

1. define host_permissions in wxt.config.ts

```
export default defineConfig({
  manifest: {
    permissions: ['storage'],
    host_permissions: [
      'http://110.42.229.221/*',
    ],
    web_accessible_resources: [
      {
        resources: ['*.png', '*.svg'],
        matches: ['<all_urls>'],
      },
    ],
  },
})
```

3. Start dev mode: `pnpm dev -b firefox`
4. checkout `<rootDir>/.output/firefox-mv2/manifest.json`

but the output miss out, `'http://110.42.229.221/*'`, just like,

```
// manifest.json file
{
  "manifest_version": 2,
  "permissions": [
    "storage",
    "http://localhost/*",
    "tabs",
  ],
  "web_accessible_resources": [
    "*.png",
    "*.svg"
  ],
}
```

### Expected behavior

expected `manifest.json` like,

```
{
  "manifest_version": 2,
  "permissions": [
    "storage",
    "http://localhost/*",
    "tabs",
+  "http://110.42.229.221/*"
  ],
  "web_accessible_resources": [
    "*.png",
    "*.svg"
  ],
}
```

### Screenshots

If applicable, add screenshots to help explain your problem.

### Environment

<!--- Run `npx envinfo --system --browsers --binaries --npmPackages wxt,vite` and paste the output below -->

```
Paste output here
```

### Additional context

use WXT 0.17.12
