### Bug report

`http.cookiejar.join_header_words` produces malformed output for values that contain an underscore together with another character that ought to be quoted (e.g. a space).

### Repro

```python
from http.cookiejar import join_header_words, split_header_words

# value contains an underscore AND a space
val = "hello_world value"
out = join_header_words([[("attr", val)]])
print(repr(out))

# round-trip
print(split_header_words([out]))
```

What I get back is something like `attr=hello_world value` — the value is not wrapped in quotes, so the space is left bare. When this string is fed back through `split_header_words` (or any other RFC-2616-ish header parser), the value gets cut off at the space and the rest is interpreted as a separate token. The round-trip is broken.

I'd expect the value to be quoted/escaped the same way it would be if it didn't contain an underscore, e.g. `attr="hello_world value"`. Plain identifier-shaped values like `hello_world` or `foo123` should still come out unquoted, as before.

I noticed this on a recent CPython; older versions (3.12 and earlier, IIRC) handle the same input correctly.
