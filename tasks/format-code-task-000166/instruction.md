# Targeted parameter substitution in map keys and values

The `copier` package provides a reflection-based deep-copy helper,
`CopyWithReplacements(src, replacementsFunc, replaceIn...)`, that clones an
arbitrary value and, while cloning, rewrites the *string* fields that the caller
opts into. A field is opted in by listing its **path** in the variadic
`replaceIn` argument, where a path is the chain of exported struct field names
joined by `.` (for example `"Spec.Template.Name"`). The literal `"*"` selects a
field and everything nested beneath it. Selected strings are rewritten by
running every `$name` token through `replacementsFunc` (the existing
`EvaluateString` behavior); unselected strings are copied verbatim.

This works for struct fields, but it is too coarse for maps. Today a map is
addressed by a single path and there is no way to say "substitute only in the
values" versus "substitute only in the keys" of that map — and map keys are in
fact never rewritten at all, regardless of what is requested.

Extend the helper so that the keys and the values of a map field can be targeted
independently:

- Appending `.Keys` to a map field's path selects that map's **keys** for
  substitution.
- Appending `.Values` to a map field's path selects that map's **values** for
  substitution.
- These compose with deeper paths the same way struct fields do: e.g. for a
  `map[string]SomeStruct` field named `Cfg`, the path `Cfg.Values.Title`
  reaches the `Title` field of each value, and `*` cascading still applies once
  a path matches.

Concretely, for a struct field `Data` of type `map[string]string`:

- `replaceIn = ["Data.Values"]` rewrites the values only; keys are left as-is.
- `replaceIn = ["Data.Keys"]` rewrites the keys only; values are left as-is.
- `replaceIn = ["Data"]` (selecting the map field itself) rewrites both keys
  and values.
- selecting neither leaves the whole map untouched.

When a key string is rewritten, the rewritten string becomes the key in the
resulting map (the map is effectively re-keyed), paired with its
(possibly-rewritten) value.

All existing behavior must be preserved: the result is always a deep,
independent copy (mutating it must not affect the source), non-map and non-string
fields are copied unchanged, string fields selected by their own path are still
rewritten, and `Copy` (the no-substitution entry point) still performs a plain
deep copy.
