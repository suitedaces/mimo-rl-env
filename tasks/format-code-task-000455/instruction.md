I have a database schema that has an enum and some tables within a postgresql schema. When I run `atlas schema diff` or `atlas schema apply` it fails to emit the `CREATE TYPE` enum definition. Everything works fine if the enum is in the default schema, this only happens if the enum is part of another schema.

Steps to reproduce:

First, create `repro.sql` with the contents below
```sql
CREATE SCHEMA test;
CREATE TYPE test.state AS ENUM ('a', 'b', 'c' );
CREATE TABLE test.the_table (
    id int4 NOT NULL,
    value test.state NOT NULL
);
```
Then run the following
```sh
touch empty.sql
atlas schema diff --dev-url docker://postgres/15/test --from file://empty.sql --to file://repro.sql --format '{{ sql . "  " }}'
```
This will print out
```sql
-- Add new schema named "test"
CREATE SCHEMA "test";
-- Create "the_table" table
CREATE TABLE "test"."the_table" (
  "id" integer NOT NULL,
  "value" "test"."state" NOT NULL
);
```
... which does not have the definition for the `test.state` enum even though `test.the_table` refers to it.

Extra notes:
- `atlas schema inspect` does emit HCL that includes the `test.state` enum.
