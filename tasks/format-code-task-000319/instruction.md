## Allow customizing the `.webp` filename rule

Most WebP converters I've used (the ones that batch-convert `.jpg` / `.png` to `.webp`) keep the original extension and just append `.webp`. So `logo.png` becomes `logo.png.webp` on disk, not `logo.webp`. This is actually the default in a lot of tools.

With the current plugin I can't make the generated CSS line up with that. For example I have:

```css
.logo {
  background: url(/logo.png);
}
```

and my actual file on disk is `/logo.png.webp`. But the plugin always rewrites the url to `/logo.webp`, which 404s.

Looking at the existing options (`modules`, `webpClass`, `noWebpClass`) there's nothing that controls how the filename is rewritten — the `.png` → `.webp` substitution is hardcoded.

Could we get an option to control how the new filename is derived from the old one? That way users whose webp files sit next to the originals as `name.png.webp` (or any other naming convention) can configure it without forking the plugin.

I'd expect the new option to be something like `rename`.

Thanks!
