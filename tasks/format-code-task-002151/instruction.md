## Switch logging library to match bundle-lib

We currently use [go-logging](https://github.com/op/go-logging) throughout the broker, but our main dependency `bundle-lib` uses [logrus](https://github.com/sirupsen/logrus). This means the broker's process emits two visually different log streams — one format/structure from our own packages and another from anything bundle-lib logs — which makes the output noisy and harder to grep / parse in production.

We should standardize on logrus across the broker so all the log output looks consistent.

A few things to keep in mind while doing this:

- The existing `LogConfig` (logfile / stdout / level / color) comes from broker config and is consumed by users out in the wild, so the config surface shouldn't change in a breaking way. Existing level strings people have in their configs (including `notice`, which logrus doesn't have natively) should keep working.
- The `Color` option can be a no-op for now if logrus's formatter doesn't make it straightforward — we can revisit coloring later. Just don't break the config schema.
- All the per-package `log` objects we currently get via `logutil.NewLog()` should be migrated; ideally we don't keep two logging libraries linked into the binary at the end of this.

Goal is: same broker behavior, same config, but one logging library end-to-end.

While we're at it, the level-string parser should probably also accept logrus's own level names (e.g. `panic`, `fatal`, `warn`) as valid inputs in addition to the existing strings, so configs written against either naming convention work.
