## `||` and `&&` don't short-circuit when one side is NaN

I'm writing alerts in Bosun and trying to use `||` as a fallback when a query returns no data. Something like:

```
$value = q("sum:my.metric{}", "5m", "")
$result = $value || 0
```

The idea is: if the query returns NaN (no data points in the window), fall back to 0 so the alert doesn't go unknown. But what I'm seeing is that `$result` is also NaN whenever `$value` is NaN — the `|| 0` part doesn't help at all.

Same thing the other direction with `&&`. I have a guard like `$hasData && $value > 100`, and when `$hasData` is 0 I'd expect the whole thing to be 0 regardless of what `$value` is. Instead, if `$value` happens to be NaN, the result is NaN and the alert misbehaves.

This makes both operators pretty useless for the most common reason you'd reach for them in a monitoring context — handling missing data. In every other language I know, `1 || anything` is true and `0 && anything` is false without ever looking at the right side, so NaN on the unused side shouldn't poison the result. Bosun's logical operators should behave the same way: if the left side alone is enough to determine the result, the right side (NaN or otherwise) shouldn't matter.
