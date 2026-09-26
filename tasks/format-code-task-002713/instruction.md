## `ALTER TYPE ... ADD VALUE` / `RENAME VALUE` on enums not picked up by sqlc

I'm using sqlc with a Postgres schema that has a few enum types. As the project evolves I want to add new variants to an existing enum, and occasionally rename one. Postgres supports this via:

```sql
CREATE TYPE mood AS ENUM ('happy', 'sad');

-- later, in a follow-up migration:
ALTER TYPE mood ADD VALUE 'ok';
ALTER TYPE mood ADD VALUE IF NOT EXISTS 'ok';
ALTER TYPE mood RENAME VALUE 'sad' TO 'unhappy';
```

When I feed a schema file containing these statements to sqlc, the generated code for the enum type doesn't reflect the new / renamed values — it's as if the `ALTER TYPE` lines weren't there. The values sqlc knows about are still just whatever was in the original `CREATE TYPE ... AS ENUM (...)`.

It would be great if sqlc handled these statements the same way it already handles `CREATE TYPE ... AS ENUM` and `DROP TYPE`, so that splitting schema changes across multiple migration files works naturally for enums.

A couple of behaviors I'd expect, just from how Postgres itself behaves:

- Adding a value that already exists should be an error, unless `IF NOT EXISTS` is used.
- Renaming a value that doesn't exist, or renaming to a value that already exists, should be an error.
- Altering a name that isn't actually an enum type should fail rather than silently succeed.
