# PostgreSQL `UPDATE ... FROM` and `DELETE ... USING`

The PostgreSQL query builder (the package published as `sqorn-pg`) currently
treats every `.from(...)` call the same way: when building an `UPDATE` or
`DELETE`, all the referenced tables are crammed into a single comma-separated
table list. That produces invalid SQL for the common case where you want to
join against another table while updating or deleting rows.

Postgres has dedicated syntax for this:

- `UPDATE target SET ... FROM other_tables WHERE ...`
- `DELETE FROM target USING other_tables WHERE ...`

Make the Postgres builder support these clauses by giving meaning to the order
of `.from(...)` calls when building an `UPDATE` or `DELETE` query:

- The **first** `.from(...)` call names the primary table being modified — it
  forms the `UPDATE <table>` clause for updates and the `DELETE FROM <table>`
  clause for deletes.
- **Every subsequent** `.from(...)` call contributes additional tables that are
  joined against. For an update these become a `FROM` clause; for a delete they
  become a `USING` clause. Multiple additional tables are separated by `, ` in
  the order the calls were made.

Behavioral details that must hold:

- When there is only a single `.from(...)` call, no `FROM`/`USING` clause is
  emitted at all (e.g. `update book set ...` or `delete from book`).
- Clause ordering in the rendered query is:
  - update: `update <table> set ... from <others> where ... returning ...`
  - delete: `delete from <table> using <others> where ... returning ...`
- All existing ways of naming tables in a `.from(...)` call keep working in
  both positions: bare string/template table names, aliased object tables
  (`{ alias: 'table' }`), and the `(values ...)` table produced from an array
  of row objects. Snake-casing of aliases/identifiers and parameter numbering
  are unchanged.
- The `where`, `returning`, and `set` behavior is otherwise unchanged.

Only the Postgres builder is affected.
