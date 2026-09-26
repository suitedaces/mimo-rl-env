[Metricbeat] Migrate `mysql/status` metricset to ReporterV2

Tracking the broader ReporterV2 migration in #10774. While going through the remaining metricsets that still implement the old `Fetch()` interface, `mysql/status` is one of the ones that hasn't been migrated yet.

We should update it to use `ReporterV2`, in line with the other metricsets that have already been converted.
