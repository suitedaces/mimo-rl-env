## Appending many rows containing a LIST column produces corrupted list values

I'm using the Appender API to bulk-insert into a table that has a `LIST` column (e.g. `INTEGER[]`). For small batches everything round-trips correctly, but once I push enough rows the contents of the lists I read back stop matching what I appended — the earlier rows look fine, later rows come back with wrong / garbage values inside the list.

Minimal repro (insert N rows, each with a short list, then SELECT them back):

```go
_, _ = db.Exec(`CREATE TABLE t (xs INTEGER[])`)

conn, _ := db.Conn(context.Background())
_ = conn.Raw(func(driverConn any) error {
    appender, err := NewAppenderFromConn(driverConn, "", "t")
    if err != nil {
        return err
    }
    defer appender.Close()

    for i := 0; i < 5000; i++ {
        if err := appender.AppendRow([]int32{int32(i), int32(i + 1), int32(i + 2)}); err != nil {
            return err
        }
    }
    return appender.Flush()
})

rows, _ := db.Query(`SELECT xs FROM t`)
// iterate rows -> later rows come back with values that don't match what was appended
```

If I keep the loop small (a few hundred rows) the assertion that `xs` equals what I appended passes. Bumping the row count up consistently makes later rows wrong. Same problem reproduces with other element types I tried inside the list (e.g. `VARCHAR[]`, nested lists), so it doesn't look specific to `INTEGER[]`.

Scalar / non-list columns appended the same way are fine — it's specifically the LIST payload that gets garbled at scale. I'd expect the Appender to faithfully write back whatever I gave it regardless of how many rows I push through it.
