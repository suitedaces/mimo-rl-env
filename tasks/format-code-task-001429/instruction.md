## Cell meta `row` / `col` get silently overwritten

I'm using Handsontable with a custom renderer and I store some extra info on cell meta. While debugging I noticed that reading `instance.getCellMeta(r, c)` sometimes returns `row` / `col` values that don't match what I'd expect — they look like they've been written to by something inside Handsontable rather than reflecting the data I configured.

Minimal repro of what's confusing me:

```js
const hot = new Handsontable(container, {
  data: createSpreadsheetData(5, 5),
  rowHeaders: true,
  colHeaders: true,
  // ...defaults, autoRowSize/autoColumnSize on
});

// Configure cell meta on a specific cell, including custom row/col-like info.
hot.setCellMeta(2, 3, 'row', 999);
hot.setCellMeta(2, 3, 'col', 999);

// Later, after the table has rendered once:
const meta = hot.getCellMeta(2, 3);
console.log(meta.row, meta.col); // expected: 999, 999 — actually: 2, 3
```

So whatever I write into `row` / `col` on cell meta does not survive a render. It gets clobbered with the actual coordinates of the cell. That's surprising — cell meta is supposed to be a place where I can put arbitrary properties without the framework touching them, and the user-facing API doesn't document that `row` / `col` are reserved/managed fields.

It also affects the inverse case: if I read `meta.row` / `meta.col` from a `cell: [{row, col, ...}]` config or from a renderer, I can't trust them to be the values I put there — they may have been silently replaced.

Could `getCellMeta` stop having its `row` / `col` mutated by internal machinery? I'd expect those properties on the returned meta object to belong to the user.
