# Filter account-download source data with a single reusable predicate

Our Spark-based account downloads parse an incoming request into a small
validated filter object (the model with fields like `fy`, `submission_types`,
`period`, `quarter`, `budget_function`, `budget_subfunction`, and `def_codes`).
Right now the logic that turns those filters into the actual row-level filtering
of the download source data lives away from that model and has to be duplicated
by every code path that needs it. Worse, it currently applies the disaster
emergency fund code (DEFC) filter to *every* submission type — but account
balances data has no DEFC column, so filtering account balances by DEFC is wrong
and breaks those downloads.

Move the filtering knowledge onto the request filter object itself. Add a method
to that model that, given a Spark `DataFrame` of account-download source rows and
the submission type the rows belong to, returns the DataFrame narrowed down to
only the rows that match the request:

```
filter_dataframe(dataframe, submission_type) -> DataFrame
```

A row is kept only when it satisfies **all** of the following:

1. **Fiscal year** — the row's `reporting_fiscal_year` equals the requested `fy`.

2. **Cumulative ("to date") reporting window** — agencies report either monthly
   or quarterly, indicated by the boolean column `quarter_format_flag`:
   - Monthly rows (`quarter_format_flag` is false) are kept when their
     `reporting_fiscal_period` is less than or equal to the requested period.
   - Quarterly rows (`quarter_format_flag` is true) are kept when their
     `reporting_fiscal_quarter` is less than or equal to the requested quarter.

   A request supplies *either* a period *or* a quarter, so the missing one is
   derived: when only a quarter is given, the requested period is the final
   period of that quarter (quarter × 3); when only a period is given, the
   requested quarter is the quarter that period falls in.

3. **Budget function** — when `budget_function` is set on the request, the row's
   `budget_function_code` must equal it; when it is not set, this filter is
   skipped.

4. **Budget subfunction** — when `budget_subfunction` is set on the request, the
   row's `budget_subfunction_code` must equal it; when it is not set, this filter
   is skipped.

5. **DEFC** — when `def_codes` is set on the request, the row's
   `disaster_emergency_fund_code` must be one of the requested codes — **except**
   for the account balances submission type, where the DEFC filter must be
   ignored entirely (account balances rows have no DEFC). When `def_codes` is not
   set, this filter is skipped.

The method must not depend on the order of the conditions, must return the source
DataFrame's rows unchanged in shape (only fewer rows), and must work for any
combination of the optional filters being present or absent.
