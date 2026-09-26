# Deduplicate type-alias definitions in the JSON Schema output

Our generator can emit shared, named definitions for TypeScript type aliases when
the alias-ref feature is enabled (the option that gives each referenced type alias
its own entry under `definitions`, referenced via `$ref`). That part works, but the
output is wasteful: when an alias is nothing more than a name for another *named*
type, the generator copies that target type's entire schema into the alias's
definition. For example, with the feature on, `type MyAlias = MyObject` produces a
`MyObject` definition and a second, byte-for-byte duplicate of it under `MyAlias`.
For recursive shapes this duplication is especially confusing.

Change this so that an alias which simply names another reffable type is emitted as
a `$ref` to that type's definition instead of a full copy.

Expected behavior, with the alias-ref feature enabled:

- A type alias whose target is another named type that gets its own definition
  (e.g. an interface or class) must appear under `definitions` as exactly
  `{ "$ref": "#/definitions/<TargetName>" }`, and the target type must still be
  present under `definitions` with its full schema.
- The target's full definition must be emitted regardless of whether anything else
  references it directly — i.e. the alias being a `$ref` must not cause the target's
  definition to go missing.
- A direct (non-alias) reference to a named type is unaffected: a property typed as
  the target type still points at `#/definitions/<TargetName>` and that definition is
  the full schema, never a `$ref` indirection.
- This works for recursive shapes: if the alias and its target refer to each other
  (directly or through properties), each named type appears once under `definitions`,
  the alias entry is the `$ref` to its target, and the target keeps its full
  property schema with the usual `$ref`s between them. No infinite expansion.
- Aliases of types that do not get their own named definition are unchanged. In
  particular, an alias of a primitive (e.g. `type MyString = string`) or of an
  inline/anonymous object type keeps its inline schema rather than becoming a `$ref`.

Other output (the `$schema` field, `type`/`properties`/`required` contents, root
handling, and the schema's validity against the JSON Schema meta-schema) stays as it
is today.
