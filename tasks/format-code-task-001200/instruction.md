## voltLib parser doesn't accept `PROCESS_MARKS NONE` (and `ALL` seems broken too)

I'm using `fontTools.voltLib` to parse a `.vtp` file exported from Microsoft VOLT. According to the VOLT syntax, the `PROCESS_MARKS` directive inside a `DEF_LOOKUP` block can take one of:

- `ALL` — process all marks
- `NONE` — process no marks
- a mark group name (string)
- `MARK_GLYPH_SET "..."`

A minimal lookup that triggers the problem looks like this:

```
DEF_LOOKUP "no_marks" PROCESS_BASE PROCESS_MARKS NONE DIRECTION LTR
AS_SUBSTITUTION
SUB GLYPH "a"
WITH GLYPH "b"
END_SUB
END_SUBSTITUTION
```

When I feed this to the voltLib parser it errors out on the `NONE` token — `NONE` doesn't seem to be recognized as a valid keyword after `PROCESS_MARKS` at all.

The `ALL` variant doesn't work the way I'd expect either: `PROCESS_MARKS ALL` parses without raising, but the resulting lookup looks as if `ALL` had been treated like an ordinary group name rather than the "process all marks" keyword. So in practice neither `ALL` nor `NONE` behaves correctly here, even though both are legal VOLT.

It would be great if the parser handled both keywords according to the VOLT spec, on par with how `SKIP_MARKS` and `MARK_GLYPH_SET "..."` are already handled.
