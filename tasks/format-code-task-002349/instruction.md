## `google.protobuf.Any` JSON conversion doesn't handle the `type.googleapis.com/` prefix correctly

I'm using protobuf.js to interop with another service that exchanges `google.protobuf.Any` values as JSON. Per Google's docs, the canonical JSON form looks like:

```json
{
  "@type": "type.googleapis.com/foo.Bar",
  "field1": "...",
  "field2": "..."
}
```

i.e. the `@type` URL has a prefix (default `type.googleapis.com/`) followed by the fully-qualified type name.

I'm running into two problems with this:

### 1. `fromObject` can't find the type when `@type` has a prefix

I have a `Bar` type registered in my root, and I do something like:

```js
var Any = root.lookupType("google.protobuf.Any");
var any = Any.fromObject({
    "@type": "type.googleapis.com/foo.Bar",
    "field1": "hello"
});
```

This silently fails to recognize `foo.Bar` — the wrapper falls through to the generic path and I don't get the embedded message packed in. If I drop the prefix and pass `"@type": "foo.Bar"` it works, but that's not the JSON I'm getting from the wire and not what Google's docs say I should be sending either.

I'd expect protobuf.js to look up the type by the fully-qualified name part of `@type` (the segment after the last `/`), and to keep the prefix the user provided on the resulting `type_url`.

### 2. `toObject` produces an `@type` without the Google-recommended prefix

Going the other direction:

```js
var msg = Bar.create({ field1: "hello" });
var any = Any.create({ /* wrap msg */ });
var json = Any.toObject(any, { json: true });
console.log(json["@type"]);
```

The `@type` I get back is just the bare type name (and in some cases it even has a leading `.`). According to Google's docs the canonical form is `type.googleapis.com/full.type.name`, and other implementations expect that. When I round-trip the JSON through another protobuf library it doesn't recognize the type because the prefix is missing.

I'd expect `toObject` (with `json: true`) to emit an `@type` that follows the Google convention — i.e. defaulting to the `type.googleapis.com/` prefix when none is otherwise present, and not leaving a leading dot on the type name.

Could the `Any` wrapper be updated so that JSON ↔ message conversion round-trips correctly with the standard prefixed form?
