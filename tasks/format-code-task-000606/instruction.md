## Some paragraphs fail to render with "unexpected type of element while serializing a paragraph"

I'm using libasciidoc to render some `.adoc` files to HTML. On certain documents (regular-looking paragraphs, nothing fancy), the conversion bails out instead of producing output. The error I get bubbles up from the substitution stage:

```
unexpected type of element while serializing a paragraph: '[]interface {}'
```

So the serializer for a paragraph is rejecting a line because it's not a `RawLine`, but apparently the lines that make it down to `serializeParagraph` aren't always raw — sometimes a line shows up as `[]interface{}` (presumably a line that already went through some other processing step / contains nested elements). When that happens, the whole paragraph never gets reparsed, and the document errors out.

This should just work — a paragraph whose lines have been turned into nested element slices is still a valid paragraph, and the serializer should be able to flatten it back to its textual form so the normal-paragraph substitution can reparse it like any other paragraph. It shouldn't be an error condition.

Could the paragraph serialization be made to handle that case (and ideally any reasonable nesting of raw lines inside it) instead of refusing?
