# Rework `serialize` into a compact, stable, human-readable format

Our `serialize(input)` helper (exported from the package root) turns any JavaScript value into a
deterministic string that everything else — `hash`, `isEqual`, `diff` — builds on. The current
output (things like `object:3:string:3:foo:...`) is verbose, hard to read, and inconsistent across
types. Replace it with a compact, stable, human-friendly format described below.

`serialize` takes a single value and returns a string. It must be **stable**: values that are
semantically the same must serialize to the same string regardless of insertion order. The exact
output for each kind of value is:

**Primitives**
- String → the text wrapped in single quotes: `serialize("hi")` → `'hi'`.
- Number → its literal text, including the special cases `NaN`, `Infinity`, `-Infinity`
  (e.g. `0` → `0`, `-100` → `-100`).
- Boolean → `true` / `false`.
- `null` → `null`, `undefined` → `undefined`.
- BigInt → the digits followed by `n` (e.g. `10n`).
- Symbol → its standard string form, i.e. `Symbol(<description>)`.

**Common built-ins**
- `Date` → `Date(<iso>)` using the ISO string (e.g. `Date(1970-01-01T00:00:00.000Z)`).
- `Error` → `Error(<error.toString()>)` (e.g. `Error(Error: test)`).
- `RegExp` → `RegExp(<regexp.toString()>)` (e.g. `RegExp(/.*/)`).
- `URL` → `URL(<url.toString()>)`.

**Arrays and binary data**
- Array → each element serialized in order, each followed by a comma, wrapped in square brackets:
  `[1,2,'x',3,]`. Element order is preserved.
- `ArrayBuffer`, typed arrays (`Uint8Array`, etc.) and Node `Buffer` → the constructor-style name
  followed by the byte values joined by commas in square brackets, e.g. `Uint8Array[1,2,3]` and
  `ArrayBuffer[1,2,3]`. A `Buffer` is treated as a `Uint8Array`.

**Plain objects and class instances**
- Plain object → `{key:value,...}` with entries joined by commas (no trailing comma). Keys are
  sorted so order is irrelevant: both `{a:1,b:2}` and `{b:2,a:1}` give `{a:1,b:2}`.
- Only string keys are considered; symbol keys are ignored (`{ [Symbol()]: 1 }` → `{}`).
- A class instance is the same but prefixed with its constructor name: an instance of `Test` with
  `x = 1` → `Test{x:1}`.
- If a value has a `toJSON()` method, serialize the value it returns instead, keeping the
  constructor-name prefix for non-plain types (a `Test` whose `toJSON()` returns `[1,2,3]` →
  `Test[1,2,3,]`).
- Any other object that is not directly supported but exposes an `entries()` iterator is serialized
  like an object, prefixed with its type name and with entries sorted by key
  (e.g. a `FormData` with `foo=bar`, `bar=baz` → `FormData{bar:'baz',foo:'bar'}`).
- Circular references must not loop forever: when an object is encountered again, emit `#<n>` where
  `<n>` is the index of that object in the order objects were first seen (the first object seen is
  `0`). A self-referencing `{ foo: <self> }` → `{foo:#0}`.

**Sets and Maps are order-less**
- `Set` → `Set` followed by the array form of its members, but members are sorted so the order they
  were inserted does not matter: `new Set([2,3,1])` → `Set[1,2,3,]`. Non-comparable members (e.g.
  objects) are ordered by their own serialized form.
- `Map` → `Map{key:value,...}` with entries sorted by key, like an object: a map with `z→2` then
  `a→'1'` → `Map{a:'1',z:2}`.

**Functions**
- A native function → `<name>()[native]` (e.g. `Array` → `Array()[native]`).
- Any other function → its name, then its parameter count in parentheses, then its source code,
  with line breaks (and the whitespace surrounding them) removed. For example a function declared as
  `function sum(a, b) { return a + b; }` → `sum(2)function sum(a, b) {return a + b;}`, and an arrow
  function assigned to `sum` → `sum(2)(a, b) => a + b`.

**Unsupported values**
- If a value cannot be serialized (no known handling and no `entries()` to fall back to), throw an
  `Error` whose message is `Cannot serialize <Type>`, where `<Type>` is the value's type name
  (e.g. a `Blob` → throws `Cannot serialize Blob`).

The previous `serialize` accepted an options object to tweak behavior; the new behavior is fixed and
takes only the value, so that single argument is all `serialize` needs.
