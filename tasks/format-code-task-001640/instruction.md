# Problem Statement

I’m using a queryset-backed table with `order_by=("full_name", "age")`, and my `order_full_name` method doesn’t seem to run unless `full_name` is the last sort key. With `("full_name", "age")` the rows look sorted by the normal `full_name` accessor and then `age`, but with `("age", "full_name")` I can see my custom full-name ordering take effect.

# Expected outcomes

- Queryset-backed tables created with `Table(..., order_by=(...))` should apply a column’s custom ordering hook whenever that column appears in a multi-column ordering, not only when it is the final ordering key.
- When a custom-ordered column appears before other ordering keys, the final queryset ordering should reflect the custom ordering for that column rather than falling back to the column’s normal accessor ordering.
- Multi-column ordering should preserve the requested ordering semantics around custom-ordered columns rather than preventing the custom hook from taking effect.

# Implementation notes

- The specific internal organization of table data handling, ordering state, and queryset mutation is up to the implementation.
- The fix should be observable through the existing public table construction and custom ordering hook APIs; no new public API is required.
