## Problem Statement

Hey, I'm using `GetLastNJobRuns` and `GetJobRunsFromLastNHours` to pull recent runs for a Jenkins job, and the results look off — I'm asking for the last 10 runs but sometimes get fewer, or it skips over runs I know exist. I think it happens on jobs where the build numbers aren't contiguous, such as when builds are pruned or fail to register and the visible build history has gaps. Could you fix the selectors so sparse build histories don't cause existing completed runs to be missed?

## Expected Outcomes

- Recent-run selection: `GetLastNJobRuns` should return the most recent completed runs for a job even when the job's build numbers have gaps.
- Recent-run selection: requesting more runs than are available should return the completed runs that can actually be found, without inventing or requiring missing build numbers.
- Time-window selection: `GetJobRunsFromLastNHours` should return completed runs in the requested recent time window for sparse build histories.
- Time-window selection: once the available history being considered has moved outside the requested time window, older history should not be used to backfill the result.
- Build-number access: `JobLogUtils` should expose `GetBuildNumbersForJob(job string) ([]int, error)`, and the built-in `GCSLogUtils` and `MockJobLogUtils` implementations should support it.

## Implementation Notes

- Preserve existing behavior around unfinished runs: runs that cannot be confirmed as finished should not be included in the returned run list.
- Keep the run selector behavior correct for sparse histories across supported log backends; internal helper functions, data structures, URL construction, and code organization are implementation details.
- Do not rely on missing build numbers behaving like unfinished runs.
