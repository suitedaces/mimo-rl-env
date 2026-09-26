## Version string is duplicated across many files

The version string `'24.3.0-alpha1'` is repeated in a number of places throughout the repo, and `scripts/updateVersion.js` has to keep a list of glob patterns to find them all when bumping versions:

```js
files: [
  'packages/**/version.{js,ts}',
  'packages/component-base/src/*.{js,ts}',
  'packages/field-highlighter/src/vaadin-field-highlighter.js',
  'packages/polymer-legacy-adapter/src/template-renderer-templatizer.js',
],
```

`grep -rn "'24.3.0-alpha1'"` turns up the same literal in `ElementMixin`, `FieldHighlighter`, `Templatizer`, the Lumo style element, the Material style element, and probably more as the project grows. Every time someone adds a new place that needs the version, the release script has to be taught about a new path, and it's easy to forget one and ship an inconsistent set of components.

I'd like the version literal to live in exactly one source location, so that:

- the release script only has to rewrite a single file, and
- adding new components doesn't require touching the release script at all.

There is one constraint to keep in mind: the duplicate-load detection inside `defineCustomElement` already relies on classes exposing a `version` (it reads `defined.version` and `CustomElement.version` to compare them and warn / error when two builds collide). Whatever the new arrangement is, custom element classes registered via `defineCustomElement` should still end up with a readable `.version` so that detection keeps working — I just don't want each component file to have to carry its own copy of the literal.
