# Add a `validateAllPaths` validation option for documents

Mongoose documents already let you narrow down what gets validated. For example, a schema
configured with `validateModifiedOnly: true` only runs validators on paths that were actually
modified, and callers can pass `pathsToValidate` / `pathsToSkip` to further restrict the work.

We need the opposite escape hatch: a way to force validation of **every** path defined on the
schema, regardless of what has (or hasn't) been modified.

Add a `validateAllPaths` boolean option that is accepted by both the asynchronous `validate()`
method and the synchronous `validateSync()` method (via their options object). When
`validateAllPaths` is `true`:

- Validation runs against every path declared in the schema, including paths whose values were
  never modified. This takes precedence over a schema-level `validateModifiedOnly` setting, so an
  unmodified-but-invalid path is reported as an error even when the schema would normally skip it.
- Each element of an array path is validated too, so element-level validators (e.g. `enum` on the
  items of a string array) run against every element. A failing element is reported under its
  indexed path (for example `tags.0`).
- A document whose paths are all valid still passes: `validateSync()` returns `undefined` and
  `validate()` resolves.

The option is mutually exclusive with the existing path-narrowing options. Combining
`validateAllPaths` with any of the following must raise a `TypeError` (and `validate()` must reject
with it) before any validation runs, using these exact messages:

- with `pathsToSkip` → `Cannot set both \`validateAllPaths\` and \`pathsToSkip\``
- with `pathsToValidate` → `Cannot set both \`validateAllPaths\` and \`pathsToValidate\``
- with a `validateModifiedOnly` option → `Cannot set both \`validateAllPaths\` and \`validateModifiedOnly\``

These rules apply identically to `validate()` and `validateSync()`.
