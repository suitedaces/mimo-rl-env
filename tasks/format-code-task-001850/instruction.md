## marimo mishandles SQL containing DuckDB escape string literals (`e'...'`)

I'm using marimo with DuckDB and ran into a bug when my SQL contains DuckDB's `e'...'` escape string literal — the form that lets you use `\n`, `\t`, etc. inside a string.

Minimal repro. In one cell:

```python
mo.sql(
    """
    CREATE TABLE my_table AS
    SELECT * FROM read_csv(e'/some/path/file\tname.csv')
    """
)
```

In a separate cell:

```python
mo.sql("SELECT * FROM my_table")
```

The SQL itself is perfectly valid DuckDB — if I paste the same statements into a plain DuckDB session they run without any issue.

Inside marimo, though, things don't behave normally for this cell. The relationship between the cell that creates the table and the cell that reads from it doesn't work the way it does for "normal" SQL cells — it feels like marimo isn't seeing this cell the same way it sees other SQL cells, and the surrounding behavior (reactivity, what happens when I edit/re-run the cell) gets weird.

As a sanity check: if I drop the `e` prefix and just write a plain `'...'` literal (so no escape sequences), everything goes back to working correctly. So the problem seems specific to the `e'...'` form.

It would be great if marimo handled SQL that contains `e'...'` literals the same way it handles any other DuckDB SQL.
