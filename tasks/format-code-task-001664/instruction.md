### schema `Hook` mutations don't actually reach the database

I'm using `core/database/schema` to drive DDL migrations and wanted to use `Schema.Hook` to rewrite each patch's DDL just before it's applied (in my case I want to tweak the statement for a test setup, but the same would apply to anything: adding comments, rewriting identifiers, etc.).

Roughly what I'm doing:

```go
s := schema.New(
    schema.MakePatch("CREATE TABLE foo (id INTEGER PRIMARY KEY);"),
    schema.MakePatch("CREATE TABLE bar (id INTEGER PRIMARY KEY);"),
)

s.Hook(func(i int, ddl string) (string, error) {
    // rewrite the DDL somehow
    return rewrite(ddl), nil
})

if _, err := s.Ensure(ctx, runner); err != nil {
    return err
}
```

`Ensure` returns no error and the `schema` bookkeeping table looks like it has been updated. But when I inspect the database afterwards, the tables that actually got created match the **original** DDL passed to `MakePatch`, not the rewritten DDL my hook returned. I can confirm the hook function itself is being invoked (I added a log line), it's just that whatever it returns appears to be discarded by the time patches are executed against the connection.

The documented contract for `Hook` is "returns a modified DDL that will be run instead", so I'd expect the rewritten statement to be the one actually executed, not just used internally for bookkeeping.
