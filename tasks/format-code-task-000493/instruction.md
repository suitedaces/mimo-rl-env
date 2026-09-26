## Build fails on JRuby for files that contain only front matter

I'm building a site with Awestruct on JRuby. A few of my pages are placeholders — they have a YAML front matter header (title, layout, some metadata) but no body content underneath yet. Something like a `foo.textile` that looks like:

```
---
title: Coming soon
layout: base
---
```

(nothing after the closing `---`).

When I run the build, it crashes on these files. If I add even a single line of real content below the front matter, the same file builds fine. So it seems specifically tied to "front matter only, empty body".

This is annoying because it's a perfectly reasonable thing to have during development — a stub page that's wired into the navigation but doesn't have its prose written yet — and one such file shouldn't take down the whole site generation.

I'd expect a file like this to just render to empty output and let the build move on.
