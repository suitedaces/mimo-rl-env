Multi-column `DataFrame.explode` currently requires every selected value in a source row to have the same effective length. Real tabular data often mixes repeated metadata scalars, singleton lists, empty lists, and genuinely ragged lists, forcing callers to normalize every row before exploding it. Add a keyword-only `mismatch` argument to `DataFrame.explode` so callers can choose how row-wise length mismatches are resolved.

`mismatch` accepts exactly `"raise"`, `"broadcast"`, and `"pad"`, and defaults to `"raise"`. Unknown values raise `ValueError`, including when only one column is selected. The default and explicit `"raise"` policy preserve today's behavior: multi-column values must have matching effective lengths, otherwise a `ValueError` is raised.

For the two permissive policies, determine a target length independently for each source row from the largest selected value in that row. Scalars and empty list-likes have effective length one, so a row whose selected values are all scalar or empty still produces one output row.

Under `"broadcast"`, scalars and one-element list-likes repeat to the row's target length. Empty list-likes produce missing values at every output position. A non-empty list-like whose length is neither one nor the target length is not broadcastable and must raise `ValueError`; do not silently cycle or pad it.

Under `"pad"`, scalars repeat to the target length, but list-likes never broadcast: their existing elements stay in order and any positions up to the target length are filled with missing values. This distinction means a one-element list is padded while a scalar is repeated. Empty list-likes are missing at every position.

In both permissive modes, source-row order and element order are preserved, unselected columns are repeated, and the original index labels (including MultiIndex names) are repeated unless `ignore_index=True`, in which case the result uses a fresh zero-based `RangeIndex`. Tuple column labels and MultiIndex columns remain supported. For a single selected column, every valid mismatch policy produces the same result as the existing single-column explode behavior, including scalar and empty-list handling.
