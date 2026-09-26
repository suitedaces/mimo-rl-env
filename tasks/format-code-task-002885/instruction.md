# Problem Statement

I’m using @tsed/objection and I’d like to define my model’s primary key as a UUID instead of an auto-incrementing id, but `@IdColumn("uuid")` doesn’t seem to be supported cleanly right now and the generated table doesn’t end up with a UUID primary key. It’d be great if UUID ids worked out of the box for Objection models. Also, I noticed the Objection relationships docs mention `HasOneThroughRelationship`, but I think the decorator name is `HasOneThroughRelation`.

# Expected outcomes

- UUID id columns:
  - `IdColumn` supports `"uuid"` as a valid id column type, in addition to the existing auto-incrementing id column options.
  - A TypeScript Objection model using `@IdColumn("uuid")` compiles without needing casts or type workarounds.

- Objection table generation:
  - When an Objection model declares a UUID id column with `@IdColumn("uuid")`, generated table/schema creation uses a UUID column for that model property.
  - The generated UUID id column is configured as the primary key.
  - The generated UUID id column has a default UUID value so new rows can receive UUID ids out of the box.
  - Existing supported id column types continue to generate their current primary key columns.

- Documentation:
  - The Objection relationships tutorial refers to the decorator as `@@HasOneThroughRelation@@`, not `@@HasOneThroughRelationship@@`.

# Implementation notes

- The exact internal structure, helper organization, and validation location are up to the implementation.
- Keep the behavior aligned with the existing Objection model and table-generation APIs rather than introducing a separate user-facing workflow.
- Documentation changes should be limited to correcting the public decorator name described above.
