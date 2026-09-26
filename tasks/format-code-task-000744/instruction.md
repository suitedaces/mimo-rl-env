## Problem Statement

I'm calling `instance.get_event_records` with `EventRecordsFilter(tags=...)` on an older Dagster instance and it just errors telling me to run `dagster instance migrate`, even though I'm not using a limit and I'd be fine with it scanning/filtering. Can we make tag filtering still work in that case? Also, when I do get the events back, it’d be really helpful if `EventLogEntry` exposed the materialization/observation tags and the observation directly instead of making me dig through `dagster_event`.

## Expected Outcomes

- On older, unmigrated instances, tag-filtered event record queries should still be usable when no limit is requested, and the results should respect the requested tag filters.
- On older, unmigrated instances, tag-filtered event record queries that also request a limit should fail with a clear invocation error explaining that this combination requires migrating the instance.
- `EventLogEntry.asset_observation` should provide direct access to an observation event’s asset observation, while non-observation events should not report one.
- `EventLogEntry.tags` should provide direct access to tags recorded on asset materialization and asset observation events, while unrelated event types should not report asset-event tags.

## Implementation Notes

- Preserve the existing public APIs for event record retrieval and filtering; the specific storage-query strategy and fallback location are up to the implementation.
- Existing migrated-instance behavior should remain compatible with the current event log storage paths.
