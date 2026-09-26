## Feature request: text wrapping filter for changelog templates

I'm putting together a custom changelog template (via the `template_dir` setting) and I'd like the generated `CHANGELOG.md` to stay within a fixed line width — for me around 80 characters — so the raw markdown reads cleanly in a terminal and in code review diffs.

The thing tripping me up is that commit descriptions passed into the template can be long single-line strings (especially when authors write detailed commit bodies). From inside the Jinja template I don't see any way to break them across multiple lines — the description just gets rendered as one very long line, blowing past whatever width I'm trying to hold.

Roughly what I'd like to write in the template:

```jinja
* {{ commit.descriptions[0] | <wrap_filter>(80, 4) }}
```

so that a description like

> This is a long commit message that explains in detail why the change was made and what the user-facing implications are.

comes out wrapped at ~80 chars with continuation lines indented (say by 4 spaces), ready to drop straight into a markdown bullet without any extra post-processing.

Looking through the documented changelog template filters (`convert_md_to_rst`, `read_file`, the URL helpers, etc.), I don't see anything that does this. I can of course preprocess the commit text in my own tooling before semantic-release ever sees it, but that defeats the point of being able to control the changelog's appearance entirely from the template.

Could a built-in word-wrapping filter be added to the changelog template environment? It feels like the kind of generic formatting helper that would live naturally alongside the existing ones. Something like `autofit_text_width(maxwidth, indent_size=...)` would be a natural name.
