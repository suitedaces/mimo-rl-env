## Migrate `uwsgi/status` MetricSet to ReporterV2

Tracking issue: #10774

The `uwsgi/status` metricset under `metricbeat/module/uwsgi/status` is still using the legacy `Fetch()` interface that returns `([]common.MapStr, error)`. As part of the broader effort tracked in #10774, it should be moved over to the `ReporterV2` interface so that it's consistent with the other metricsets that have already been migrated.

Heads-up: this one is a bit more involved than some of the other modules — it has more tests than usual and the module setup deviates from the typical pattern in a few places, so the migration is not a pure mechanical rename.
