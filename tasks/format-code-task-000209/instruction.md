## Problem Statement

I have a cohort that hit an error during calculation, and now it just sits there looking like it’s still calculating forever. From the API/UI I can’t tell that it failed or how many times it’s failed, and the background recalculation seems to keep picking it up again.

## Expected outcomes

- Cohort API responses expose an `errors_calculating` value so API/UI clients can see how many calculation failures have been recorded for a cohort.
- When a cohort calculation fails, the cohort should no longer appear to be actively calculating, and its recorded calculation failure count should increase.
- When a cohort calculation later succeeds, the cohort should finish calculating normally, update its successful calculation metadata, and clear its recorded calculation failure count.
- Periodic/background cohort recalculation should not keep automatically scheduling cohorts that have already failed repeatedly; cohorts with three or more recorded calculation failures should be skipped by that automatic recalculation path.

## Implementation notes

- The exact storage, validation, and error-handling structure is up to the implementer, as long as the externally observable API and recalculation behavior above are satisfied.
- Preserve existing cohort calculation behavior for successful cohorts, aside from clearing any prior recorded failure count on success.
