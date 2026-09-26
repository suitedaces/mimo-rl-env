# Catch unsupported cache `directory_layout` values during config validation

Every MapProxy cache can choose how its tiles are arranged (on disk or in object
storage) through the `directory_layout` option. Right now a bad value slips
straight through configuration validation: a typo like `tmss`, or wrong casing
like `TMS`, is accepted at validation time and only blows up much later as an
obscure `ValueError` while the cache is actually being built — which is hard to
trace back to the offending line in the config.

Make the configuration check catch this up front. The same validation pass that
already reports problems such as unknown grids and missing sources should also
flag any cache that is configured with an unsupported `directory_layout`.

Expected behavior:

- The supported layouts are `tc`, `mp`, `tms`, `reverse_tms`, `quadkey`, and
  `arcgis`. A cache that uses one of these — or that does not set
  `directory_layout` at all — must not produce any error.
- A cache whose `directory_layout` is anything else must produce exactly one
  validation error for that cache. The reported message must identify the
  offending cache by its name and include the invalid value. Matching is exact
  and case-sensitive, so values like `TMS` or `Quadkey` are invalid.
- Each offending cache is reported on its own, so two misconfigured caches
  result in two errors.
- Otherwise-valid configurations must keep validating exactly as before; this
  check must not introduce any spurious errors.
