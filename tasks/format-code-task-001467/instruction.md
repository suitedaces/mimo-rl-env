# Problem Statement

I’m building a Dashboard with the built-in HTML component and I already have the content as an HTML string. Right now it feels like I have to turn that into the elements structure or make a custom component just to render it. Could the HTML component accept a plain HTML string directly so I can drop in markup like a heading without that extra conversion?

# Expected outcomes

- Built-in Dashboard HTML components configured with `type: 'HTML'` should accept an `html` property whose value is a plain HTML string.
- When an HTML component is configured with `html`, the component should render the corresponding markup into its dashboard cell, including ordinary element structure, text, and attributes from the string.
- Existing HTML component configurations that use the `elements` array should continue to render as before.
- Dashboard documentation for the built-in HTML component should describe `html` as a supported way to define component content.
- Dashboard documentation and examples for custom HTML components should no longer imply that a custom component is required just to render an HTML string in a built-in HTML component.

# Implementation notes

The exact parsing path, data structures, and internal placement of the conversion logic are left to the implementer. Preserve the existing public Dashboard configuration style and compatibility with current HTML component usage while adding support for the new string-based content option.
