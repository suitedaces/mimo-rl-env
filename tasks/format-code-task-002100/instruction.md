### Feature request: way to reset rows on an existing Table

I'm using `tablewriter` in a small CLI that periodically re-renders a status table (think a refreshing dashboard view). The header, borders, alignment and column separators stay the same every tick — only the row data changes.

Right now my loop looks roughly like this:

```go
table := tablewriter.NewWriter(os.Stdout)
table.SetHeader([]string{"Name", "Status", "Count"})
table.SetBorder(true)
table.SetAlignment(tablewriter.ALIGN_LEFT)
// ... a bunch more config ...

for {
    rows := fetchLatest()
    for _, r := range rows {
        table.Append(r)
    }
    table.Render()

    // now what? I want to throw away these rows and Append fresh ones
    // next iteration, but there's no way to do that.
    time.Sleep(time.Second)
}
```

As far as I can tell from the public API, once you've called `Append` (or `AppendBulk`) there's no way to drop those rows again. Same story for `SetFooter` — once it's set, it's set. So on the next iteration the previous rows are still in the table and everything just keeps growing.

My only workaround is to throw the whole `Table` away and build a new one from scratch every tick, which means duplicating all the header/border/alignment setup code, or stuffing it into a helper. That feels wrong for what is essentially "render the same table shape, with different data."

It would be really useful to have a way to clear the previously appended rows (and ideally the footer too) on an existing `Table` so the configuration can be reused across renders. Would you accept a PR for this?

I was thinking the methods could be named something like `ClearRows()` and `ClearFooter()`.
