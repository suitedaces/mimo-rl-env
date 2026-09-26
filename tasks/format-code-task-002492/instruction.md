# Controlled cell updates for `cellEdit`

The table component keeps its own copy of the row data and renders from it. Today, when a
cell edit is committed the data handling is rigid: there is no way for an application to
veto the change, substitute a different value, or run an asynchronous save before the table
reflects the new value.

Extend the `cellEdit` configuration with an `onUpdate` callback that lets the application
take control of what happens when a cell edit is committed. `onUpdate` is invoked with
`(rowId, dataField, newValue)` where `rowId` is the value of the row's `keyField`,
`dataField` is the edited column's field, and `newValue` is the value the user entered.

The value returned from `onUpdate` decides how the table applies the edit:

- **No `onUpdate`, or it returns `undefined`/any plain truthy value** — the table updates its
  own data so that the edited row's `dataField` becomes `newValue`.
- **Returns `false`** — the table does **not** touch its own data at all. This lets an
  application drive the data externally (for example through its own store) while the table
  stays out of the way.
- **Returns a plain object that has a `value` property** — the table updates its own data using
  that object's `value` instead of `newValue`. This is for the case where a save round-trip
  produces a corrected/normalized value that should be displayed.
- **Returns a Promise** — the table waits for it to settle:
  - If it resolves to a plain object with a `value` property, the table stores that `value`.
  - If it resolves to anything else, the table stores `newValue`.
  - If it rejects, the table leaves its data unchanged.

The existing `beforeSaveCell(oldValue, newValue, row, column)` hook still fires before the
update is attempted. The `afterSaveCell` hook fires only after the table has actually applied
an update to its own data — so it must not fire when `onUpdate` returns `false` or when a
returned Promise rejects.

Editing should end (the cell returns to its normal, non-editing rendering) whenever the table
applies an update to its data.
