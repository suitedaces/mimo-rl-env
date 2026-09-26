## `getValueNode` / `getValueNodes` can't address individual items inside a repeated field

I'm using the TS `lilac` library to render rows in our web UI. After `deserializeRow`, I want to look up specific cells in the tree by path — including elements inside repeated (array) fields.

Suppose I have a schema with a repeated field `items` where each item has a `name`. After deserializing a row, I'd expect to be able to do something like:

```ts
const row = deserializeRow(rawRow, schema);

// First item's name
getValueNode(row, ['items', '0', 'name']);

// All items' names
getValueNodes(row, ['items', '*', 'name']);
```

What actually happens:

1. `getValueNode(row, ['items', '0', 'name'])` returns `undefined`. In fact any concrete-index path into a repeated field returns `undefined`.
2. If I dump every value node with `listValueNodes(row)` and inspect their `L.path(...)`, every element under `items` reports the same path — something like `['items', '*', 'name']`. There's no way to tell two array elements apart, so even iterating the list manually doesn't help me find "the 0th item".
3. `getValueNodes(row, ['items', '*', 'name'])` also returns nothing useful, because the comparison is strict equality and (separately) once I fix the per-element paths I'd still want the `*` form to work as a query that pulls every element.

So I'm stuck — there's no path I can pass to `getValueNode` that addresses a single element of a repeated field, and a wildcard query doesn't pull all of them either.

The behavior I'd expect:

- Each element inside a repeated field is individually addressable in the deserialized row.
- A path that uses `*` as the index segment (matching how schema field paths are written) should match every element of that repeated field when querying values / fields.

Same issue applies to `getField(schema, path)` if I pass a concrete-index path — it doesn't find the field, because schema field paths use `*` and the lookup is strict equality.

While we're touching this area, it would also be handy to expose a small helper like `listFieldParents(field, schema)` that returns the chain of parent schema fields for a given field — useful when walking up the tree from a leaf.
