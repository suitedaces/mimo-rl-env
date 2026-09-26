## Feature request: customize the name used for each glyph in the generated CSS

I'm using `webfont` to bundle a set of SVG icons into a webfont and emit a CSS stylesheet via the built-in `css` template:

```js
webfont({
  files: 'src/svg-icons/**/*.svg',
  fontName: 'my-font',
  template: 'css'
}).then(/* write result.styles to disk */);
```

By default, the class name for each icon in the generated CSS is derived from the SVG file name (e.g. `home.svg` → `.my-font-home`). That's fine as a default, but I'd like to control how those per-icon names look in the final CSS without changing my source files.

Concrete cases I run into:

- The SVGs come from an external icon set / a designer hand-off, so renaming the files just to fit my CSS naming convention isn't practical (it goes out of sync the next time we re-import).
- Sometimes I want all icon classes to share a common suffix (e.g. `-icon`) so they don't collide with other utility classes in the project.
- Sometimes I want to massage the name a bit (case, separators, drop a prefix the icon set ships with, etc.).

Right now the only workarounds I can see are:

1. Rename every SVG file — fragile, as above.
2. Throw away the built-in `css` template and maintain my own template just to change how the name is rendered — way too much overhead for what should be a one-line tweak.
3. Post-process the generated CSS string with a regex — works but feels wrong, and breaks if the template ever changes.

It would be really helpful if `webfont` exposed a hook that lets the caller transform each glyph's metadata (its name in particular) before the styles template is rendered, so I can plug in arbitrary logic from my own config. Something I can pass alongside the existing options to `webfont({ ... })` and have it apply to every glyph that goes into the template.

Would you be open to adding that? A new option along the lines of `glyphTransformFn` would work well for me.
