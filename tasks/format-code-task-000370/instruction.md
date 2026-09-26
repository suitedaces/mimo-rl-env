## Problem Statement

I'm passing `cutoff_time` into `Entity.head()` / `EntitySet.head()`, but the rows I get back still include records after that timestamp. I also hit weird behavior with `Variable.head(cutoff_time=...)`: sometimes it looks like the cutoff is ignored, and in one case it errored instead of returning the expected variable values.

## Expected Outcomes

- `Entity.head(n=..., cutoff_time=...)` and `EntitySet.head(entity_id, n=..., cutoff_time=...)` should apply the cutoff to the returned data before limiting to the requested number of rows.
- Timestamp-style cutoffs should exclude rows at or after the cutoff time.
- Tabular cutoffs supplied as a two-column pandas `DataFrame` should constrain results using the provided instance identifiers and their associated cutoff times.
- `Variable.head(n=..., cutoff_time=...)` should return the requested variable as a single-column `DataFrame` while honoring the same cutoff behavior.
- Invalid `cutoff_time` inputs should fail clearly with `ValueError` and the message `cutoff_time must be None, a Datetime, a pd.Timestamp, or a pd.DataFrame`.

## Implementation Notes

The filtering location, helper structure, and internal data flow are implementation details. Preserve the existing public API shape for `Entity.head`, `EntitySet.head`, and `Variable.head`, and make the externally visible returned data and errors match the behaviors above.
