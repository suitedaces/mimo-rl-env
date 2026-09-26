## geomap widget should support formulas and functions

Most of the dashboard widget types (`timeseries_definition`,
`query_value_definition`, etc.) accept a `request` configured in the
formulas-and-functions style — one or more `query { ... }` blocks plus
optional `formula { ... }` blocks. `geomap_definition` doesn't: its
`request` only exposes the older `q`, `log_query`, and `rum_query`
arguments.

This means I can't move my geomap widgets to formulas/functions even
though the Datadog API and UI support it. Here is the kind of `request`
body I'd write for a timeseries widget today:

```hcl
request {
  query {
    metric_query {
      name        = "q1"
      data_source = "metrics"
      query       = "avg:system.cpu.user{*} by {country-iso-code}"
    }
  }
  formula {
    formula_expression = "q1"
  }
}
```

If I drop the same body into `geomap_definition.request`, `terraform plan`
rejects it — the geomap request schema doesn't know about `query` or
`formula`.

Could the geomap widget's request gain the same formula+query support that
other widget types already have? Ideally with the same set of query
sources (metric / events platform / process queries) so the config looks
consistent across widget types, and so the existing `formula` options
(alias, limit, etc.) work the same way here.
