## Backslashes in quoted strings aren't escaped/unescaped properly

I ran into this while setting display names that happen to contain a backslash. For example a name like `Foo\Bar "baz"` — perfectly legal content for a quoted-string per RFC-822, but mail doesn't seem to handle the `\` character correctly when wrapping/unwrapping quoted strings.

A small repro using the helpers directly:

```ruby
include Mail::Utilities

s = 'Foo\\Bar'           # the literal 4-character string: F o o \ B a r... wait, 7 chars
puts s                   # => Foo\Bar
puts dquote(s)           # I'd expect "Foo\\Bar" (i.e. the backslash escaped inside the quotes)
puts unquote(dquote(s))  # I'd expect to get back exactly Foo\Bar
```

What actually happens is that `dquote` only escapes `"` and leaves `\` alone, so the produced quoted string isn't a valid RFC-822 quoted-string for inputs containing backslashes. And `unquote` just strips the surrounding `"..."` without undoing any `\`-escaping at all, so a string that was correctly escaped on the way in comes back out with stray backslashes.

The net effect is that `dquote` / `unquote` aren't proper inverses of each other once the input contains `\` or `"`, and values like `Foo\Bar` or names containing nested quotes get corrupted on round-trip.

Per RFC-822 §3.4.5, both `\` and `"` need to be quoted-pair-escaped inside a quoted-string, and on the reverse direction the escaping has to be undone. Could the quoting helpers be fixed so that any string round-trips cleanly through `dquote` → `unquote`, including ones containing backslashes?
