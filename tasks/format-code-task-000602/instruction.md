## Feature request: per-call field overrides for `FakeData`

I'm using `faker` to populate structs in unit tests. Most of the time the default tag-based generation is exactly what I want, but I keep running into two cases where I need finer control on a **per-call** basis:

1. **Some fields shouldn't be randomized at all.** Typical example is a primary-key-ish field that I want to leave at its zero value (or set myself afterwards), or a field whose zero value carries semantic meaning for the test. Today `FakeData` fills every exported field, so I end up zeroing them out again right after the call, which is noisy.

2. **A specific field needs a value from a constrained set.** For example a `Status` field that must be one of a handful of valid enum strings, or an `Age` that must satisfy some test-specific invariant. The `oneof` tag covers some of this, but I don't want to bake test-only constraints into the struct tags of my production types. I'd like to supply a generator function for that one field, just for this call.

What I'd like is something roughly like:

```go
type User struct {
    ID     int64
    Name   string
    Status string
}

var u User
err := faker.FakeData(&u, /* tell faker to skip ID and to use my fn for Status */)
```

…where the "skip these fields" list and the "use this function for that field" mapping are passed in at the call site, so they don't leak into the struct definition and don't affect other tests / other calls to `FakeData`.

### Why not the existing extension points?

- `AddProvider` / `RemoveProvider` register a provider against a **tag name**, globally. That means I'd have to (a) put a custom tag on my struct field and (b) mutate global state in tests, which is ugly and racy when tests run in parallel.
- Struct tags like `faker:"-"` work, but again they live on the type, not on the call. I don't always want that field skipped — only in this particular test.

### Expected behavior

- A way to pass, at call time, a set of field names that `FakeData` should leave alone (no randomization, original/zero value preserved).
- A way to pass, at call time, a mapping from field name to a user-supplied function that produces the value for that field. If the function returns an error, `FakeData` should surface it rather than silently swallowing it.
- Existing call sites (`faker.FakeData(&x)` with no extra arguments) should keep working unchanged.

Happy to help review if someone picks this up.

The shape I have in mind is something like `faker.FakeData(&u, faker.WithFieldsToIgnore("ID"), faker.WithCustomFieldProvider("Status", myStatusFn))`.
