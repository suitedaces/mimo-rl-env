## Reaper silently does nothing when `source_for_total_space` / `source_for_used_space` is misconfigured

We configure some of our RSEs to compute free space from a non-default source by setting the RSE attributes `source_for_total_space` and `source_for_used_space` (instead of the default `storage`). This works fine when the source name actually matches one of the usage entries reported for the RSE.

The problem: if the configured source name doesn't exist in that RSE's usage (typo, source not yet publishing, source got renamed, etc.), the reaper just... does nothing on that RSE. No replicas get deleted, free space never recovers, and **there is nothing in the reaper log to tell us why**. From the operator's point of view the RSE looks healthy, reaper appears to be running normally on it, but space keeps filling up.

To reproduce:
1. Pick an RSE whose usage table only reports one source, e.g. `storage`.
2. Set `source_for_total_space=foo` on it (where `foo` is anything not in its usage entries).
3. Run the reaper against that RSE with replicas that have tombstones and should be reaped.

Expected: at minimum a clear log message saying that the requested source can't be found on this RSE, so an operator can immediately tell it's a configuration issue. Ideally the reaper would also not be completely stuck — for an RSE in this state it would still be reasonable to clean up obsolete/expired replicas (the things that don't need a free-space calculation to decide on), instead of skipping the RSE entirely.

Right now we only notice this when the RSE shows up as full in monitoring, and then we have to go diff the RSE attributes against the usage table by hand to figure out what's wrong. A warning in the reaper log would save a lot of time.
