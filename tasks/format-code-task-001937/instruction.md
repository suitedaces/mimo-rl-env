# Problem Statement

I’m using Turndown to convert HTML that has inline `<code>` snippets, and I need a way to keep the spacing inside those snippets exactly as written. For example, something like `<code>git   log</code>` shouldn’t turn into a code span with the spaces collapsed, because in my docs that spacing can be intentional. It would be great if I could opt into treating inline code more like preformatted text during conversion.

# Expected outcomes

- Configuration:
  - `TurndownService` should accept a `preformattedCode` option.
  - The option should be opt-in: when `preformattedCode` is not provided, or is set to `false`, existing inline `<code>` whitespace handling should remain unchanged.
  - When `preformattedCode: true` is provided, inline `<code>` content should be converted without collapsing or trimming the whitespace that belongs to the code snippet.

- Inline code conversion:
  - Runs of spaces inside inline `<code>` should be preserved in the generated Markdown code span when `preformattedCode: true`.
  - Leading and trailing whitespace that is part of an inline `<code>` snippet should remain part of the generated Markdown representation when `preformattedCode: true`.
  - Inline `<code>` snippets should still behave as inline code in the Markdown output; surrounding inline content should continue to be converted normally.

- Surrounding inline content:
  - Enabling `preformattedCode` should not cause whitespace inside adjacent `<code>` elements to incorrectly control trimming decisions for neighboring non-code inline content.
  - Existing output behavior for non-code content and for non-enabled inline code conversion should remain compatible with current behavior.

- Documentation:
  - The README options documentation should mention `preformattedCode`, indicate that it is optional, and show that its default value is `false`.

# Implementation notes

The exact implementation approach is up to you. Preserve the public Turndown conversion API style, keep the new behavior opt-in, and avoid changing unrelated Markdown output behavior.
