## Alerts on non-numeric column data behave incorrectly

I have an alert configured with a numeric comparison (e.g. selector = `first`, op = `<`, threshold = `4`), but the column it points at sometimes contains non-numeric data (string values, or numbers stored as strings that occasionally aren't valid numbers). The alert evaluation does the wrong thing in this case.

What I'm seeing:

1. **Alert state ends up as OK when it really shouldn't be evaluatable.** If the column value is something like `"test"` and the operator is `<` against threshold `4`, there's no meaningful way to decide whether the condition is true or false — but the alert silently lands in the OK state, which is misleading because it looks like the alert was successfully checked and passed. I'd much rather see this surfaced as `UNKNOWN` so I know the alert couldn't actually be evaluated against the data.

2. **`min` / `max` selectors break on non-numeric data.** When I switch the selector to `min` or `max`, and the column has any value that isn't a number, the evaluation goes wrong as well — again, an alert that we can't reasonably evaluate shouldn't quietly resolve to OK.

3. **The "Max column value is …" / "Min column value is …" hint in the alert editor shows `NaN`.** In the Criteria UI, when I pick a column that has any non-numeric entries, the hint at the bottom shows `NaN` instead of a useful number. It would be much more helpful if it just showed the actual max/min over the values in that column that are numbers, ignoring the ones that aren't.

So basically: alerts that point at columns containing non-numeric data should be treated as not-evaluatable (UNKNOWN) rather than OK for ordering comparisons, and the editor hint shouldn't get poisoned by a single bad cell. Equality / inequality checks against non-numeric values are obviously still meaningful and should keep working.
