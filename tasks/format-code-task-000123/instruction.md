## Updating a formatted field — the new value can't be found by `filterByText` over all fields

I have an `igDataSource` (used by igGrid) where one of the schema fields has a `formatter` function set up — in my case it's a number column that gets formatted into a currency string for display.

Roughly the setup looks like this:

```js
var ds = new $.ig.DataSource({
    dataSource: products,
    schema: {
        fields: [
            { name: "ProductID", type: "number" },
            { name: "Name", type: "string" },
            {
                name: "Price",
                type: "number",
                formatter: function (val) { return "$" + val.toFixed(2); }
            }
        ]
    }
});
ds.dataBind();
```

When the data is first loaded, `filterByText` over all fields works as expected — searching for the formatted string of the `Price` column (e.g. `"$19.99"`) matches the row that has `Price: 19.99`.

The problem shows up after I edit a formatted field. If I call `updateRow` to change `Price` on some row from `19.99` to `42.50` and commit the transaction, then call `filterByText("$42.50")` over all fields, **the updated row is not returned**. The old value still matches (until I commit), and the new formatted value matches nothing — even though the underlying data has clearly been updated (I can see the new value in the grid, and filtering on the raw `Price` field directly works fine).

So `filterByText` across all fields seems to be searching against a stale formatted representation of the rows for any field that has a `formatter` — initial bind is fine, but after a commit on an updated row the formatted view for that row is out of sync with the actual data.

Could `filterByText` over all fields stay consistent with the current state of the data source after edits on formatted columns? Right now the only workaround I have is to re-bind the data source after every commit, which obviously defeats the point of transactions.
