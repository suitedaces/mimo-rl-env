## Meta refresh tag URLs are not being archived correctly

I'm using Zeno to archive some pages that rely on `<meta>` refresh tags to redirect users to the actual content, e.g.:

```html
<meta http-equiv="refresh" content="0; url=https://example.com/real-page">
```

I expected Zeno to pick up `https://example.com/real-page` as an asset to archive (the same way it would follow other links/redirects on the page), but that doesn't seem to be happening — the redirect target ends up missing from my archive.

Looking at the archived output, it seems like the current handling of the meta tag's `content` attribute doesn't really understand this format. It looks like it just treats the whole `content` string as a candidate URL if it contains `http`, which means a value like `0; url=https://example.com/real-page` doesn't get processed as a proper URL (it's not a valid URL on its own).

It would be great if the meta tag handling could recognize the standard `content="<delay>; url=<actual url>"` format used by refresh tags and pull the real URL out of it, so those targets actually make it into the archive.

The existing behavior for meta tags that just have a plain URL in `content` (e.g. things like `<meta property="og:image" content="https://example.com/img.png">`) should keep working as before.
