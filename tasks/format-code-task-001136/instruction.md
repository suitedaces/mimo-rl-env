Automatic migration generation becomes ambiguous as soon as several tables or columns are renamed together. `SchemaDiffer` currently asks pairwise yes/no questions (or applies one `auto_input` answer globally), so non-interactive callers can't say which old object corresponds to which current object. Add explicit rename hints to make these diffs scriptable while preserving the existing interactive behavior.

Extend the public `SchemaDiffer` constructor with two optional dictionary arguments:

- `table_rename_hints` maps an old class name from `schema_snapshot` to its new class name in `schema`.
- `column_rename_hints` maps each current table class name to another dictionary whose old snapshot column names map to current column names. Column hints are therefore table-scoped, and when a table is also renamed they use its new/current class name.

A valid table hint is authoritative even when the two tables have no columns in common. It must be resolved before heuristic rename detection and must not call `input()` for the hinted pair. Emit the existing `manager.rename_table(...)` statement using the old table's class name and tablename and the current table's class name and tablename. Treat that pair as one existing table throughout the rest of the diff: don't also create or drop it, and don't emit its columns as columns of a newly created table. Objects not covered by a hint must remain ordinary add/drop candidates.

A valid column hint emits the existing `manager.rename_column(...)` statement with the current table class name and tablename. The old and new names must not also appear in drop/add-column statements, while unrelated column additions and removals must still be reported. If the renamed column's type or parameters changed at the same time, also emit the normal `manager.alter_column(...)` statement, addressed by the new column name and current table identity, with the current and snapshot definitions represented as the new and old definitions respectively. This must also work when the containing table is renamed in the same diff.

Make rename output deterministic: hinted table rename statements are ordered lexicographically by current class name, and hinted column rename statements by current class name then new column name, regardless of schema or dictionary insertion order. Generating statement groups repeatedly must return the same results and must not change any supplied table's class name or tablename, or any supplied column's name, in either `schema` or `schema_snapshot`.

Validate hints when `SchemaDiffer` is constructed. Raise `ValueError` if a table hint names a missing old or current class, if two old tables target the same current table, if a column hint names a missing current table, old column, or new column, or if two old columns in one table target the same new column.

Calls which omit both hint arguments must retain the current `auto_input` / interactive rename behavior and existing add, drop, rename, and alter statement formats.
