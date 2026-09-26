I'm parsing GDB MI output with `gdbmiparser.parse_response`, and the escape sequences in the strings aren't coming through right. For example, when I parse `~"a\nb"`, the payload comes back as the literal `a\nb` with the backslash still in it, instead of an actual newline. Same kind of thing with `\t`. And when there's an error like `^error,msg="some error\non multiple lines\twith escapes"`, the `msg` I get back is even worse — the backslashes just vanish, so `\n` turns into a literal `n` and `\t` into `t`. I'm also seeing octal escapes like `\040` left as-is. Makes it pretty hard to log or display GDB's output cleanly.

Expected outcomes:
- Result records parsed through `gdbmiparser.parse_response` should preserve their normal parsed structure, and escaped string fields should contain the characters represented by GDB MI escape sequences rather than losing backslashes or leaving escapes literal.
- Textual stream records parsed through `gdbmiparser.parse_response` should return payload text with GDB MI escape sequences interpreted into the corresponding characters.
- GDB MI string escapes, such as the newline/tab and octal examples above, should be handled consistently wherever escaped MI strings are parsed.

Implementation notes:
- The parsing API and existing response shapes should remain compatible with current callers.
- The internal organization of the unescaping logic is up to the implementer; focus on externally observable parsed values rather than any particular helper, module layout, or parsing strategy.
