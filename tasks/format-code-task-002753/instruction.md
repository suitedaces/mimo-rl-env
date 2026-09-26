## JSON field with a falsy value (`false`, `0`) disappears in the entry editor

I have a content type with a JSON field on it. When I save a falsy-but-valid JSON value to that field and reopen the entry in the content manager, the editor doesn't show the value I saved — it looks like a brand-new empty field.

### Repro

1. Create a content type, e.g. `Setting`, with a JSON field called `data`.
2. Create an entry and set `data` to `false`. Save.
3. Reopen the entry from the content manager.

The JSON editor for `data` is empty. There's no `false` in it. If I save again at this point I lose the original value entirely.

Same thing happens if I store `0` instead of `false`.

For comparison: storing `{ "foo": 1 }` or `[1, 2, 3]` works fine — the editor displays them as nicely formatted JSON text when I reopen the entry.

### What I'd expect

A JSON field is supposed to accept any valid JSON value. `false` and `0` are valid JSON, so reopening the entry should show me the literal JSON text I previously saved (i.e. `false`), the same way it would for an object or an array. Otherwise these values are basically un-editable from the admin UI.
