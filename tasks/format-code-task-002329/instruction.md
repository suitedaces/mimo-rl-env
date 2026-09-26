## Prettier reformats expressions inside template literal `${...}` placeholders, producing ugly output (and seemingly changing the string itself)

When I have a template literal whose placeholders contain non-trivial expressions (chained calls, multi-argument function calls, ternaries, object literals, etc.), prettier reflows the code inside `${...}` as if it were a normal expression, which makes the whole template literal break across many lines.

A small example of what I'm writing:

```js
const msg = `User ${getUser(id, opts).name} logged in at ${formatDate(when, "HH:mm")}`;
```

After running prettier, the placeholders get wrapped/indented and the whole string explodes into something like:

```js
const msg = `User ${
  getUser(id, opts)
    .name
} logged in at ${
  formatDate(
    when,
    "HH:mm"
  )
}`;
```

Two things bother me about this:

1. It looks really bad. A template literal is meant to read as one piece of text with a few holes in it; once each `${...}` is allowed to span multiple lines with its own indentation, the whole thing stops reading like a string at all.

2. Template literals are sensitive to whitespace — every character between the backticks ends up in the resulting string. The extra newlines and indentation that prettier inserts inside `${...}` boundaries appear to leak into the actual string value, so the formatted code doesn't just look different, it can produce different runtime output than the unformatted version. That's surprising for a formatter.

I'd expect prettier to leave the expressions inside `${...}` alone in terms of line breaks — keep each placeholder on one line and don't make the template literal grow vertically just because the expression inside a placeholder happens to be long. (If the expression itself already contains something that genuinely has to break onto multiple lines, that's fine; but prettier shouldn't be the one introducing the breaks.)
