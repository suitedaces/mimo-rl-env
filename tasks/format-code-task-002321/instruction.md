**Dynamic `import()` gets broken across lines with a trailing comma**

When I have a long dynamic import for code splitting, prettier breaks the argument onto its own line and adds a trailing comma when `trailingComma` is set to `"all"`. For example:

```js
import("some/long/path/to/a/module/that/does/not/fit/on/one/line.js");
```

gets formatted as:

```js
import(
  "some/long/path/to/a/module/that/does/not/fit/on/one/line.js",
);
```

That trailing comma is a syntax error — `import(...)` only takes a single argument and engines/parsers reject the trailing comma.

For comparison, `require("some/long/path/to/a/module/that/does/not/fit/on/one/line.js")` is left on a single line by prettier specifically to avoid this kind of issue. I'd expect `import(...)` to be treated the same way: keep the single string argument inline rather than breaking it and emitting an invalid trailing comma.

Repro: any prettier config with `--trailing-comma all` and a dynamic import whose argument is long enough to overflow `printWidth`.

The same should also hold when the dynamic import is chained, e.g. `import("...long...").then(exports => {})` — the long string argument shouldn't be broken with a trailing comma there either.
