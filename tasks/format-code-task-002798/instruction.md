I want `Typewriter` to accept strings with HTML markup in `typeString()` and `pasteString()` and turn them into real nested DOM nodes instead of typing the angle brackets as literal text.

When I call `typeString('Hello <strong>world</strong>!')` on an instance, the wrapper should end up with plain text nodes for the text around the markup and a real `<strong>` element containing `world` in the right place.

When I call `pasteString('Hello <strong>world</strong>!')`, it should paste the same structure in one queued paste operation rather than flattening the markup.

Nested markup should work too, and an optional parent node argument should let the HTML content be inserted inside that node instead of always using the top-level wrapper.

The behavior should be the same every time for the same input, and ordinary plain-text strings should still follow the existing typing and pasting paths.
