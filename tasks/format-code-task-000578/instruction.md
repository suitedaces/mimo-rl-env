## OpenTSDB `dropcounter` rate option not supported

OpenTSDB supports a `dropcounter` rate option (in addition to `counter`) which behaves like `counter` but drops data points where the counter appears to have reset, instead of emitting a huge negative/wrap-around value. This is very useful for metrics from processes that restart and reset their counters — `counter` with a `counterMax` doesn't always cut it because we don't know the real max.

When I write a bosun query using it, e.g.

```
sum:rate{dropcounter}:os.cpu
```

bosun doesn't handle it as a `dropcounter` — it just treats the rate options block as if `dropcounter` weren't a counter at all, and round-tripping the parsed `Query` back to a string loses the option entirely. So I can't take advantage of this OpenTSDB feature from bosun.

Would be great if `opentsdb.ParseQuery` (and the corresponding `Query.String()`) understood `dropcounter` the same way it understands `counter`, and carried the information through on the `RateOptions` so it ends up in the JSON sent to OpenTSDB.

I'd expect a new boolean field on `RateOptions` (something like `DropResets`) to carry this through alongside the existing `Counter` flag.
