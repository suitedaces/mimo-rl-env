## `TimeRange::isInSameRange` gives wrong results for weekly sessions whose start day == end day

I have a FIX session configured to run weekly — `StartDay` and `EndDay` are set to the same weekday, with `StartTime`/`EndTime` defining the cutover time of day. So the session opens once a week at e.g. Sunday 17:00 and stays open until the same time the following Sunday (full week, single reset per week).

I'm using `TimeRange::isInSameRange(time1, time2)` (via the per-session helper) to figure out whether two `UtcTimeStamp`s fall inside the same weekly session — this is how I correlate sequence numbers / decide whether a previous day's state should still apply.

The results are wrong around the weekly reset.

Concretely, with a Sun 17:00 → Sun 17:00 session:

- Two timestamps that straddle the Sunday 17:00 reset (e.g. Saturday afternoon and the following Monday morning) **should** be in different ranges, but `isInSameRange` reports them as the same range.
- A timestamp from just before reset on Sunday and one from just after reset on the same calendar Sunday **should** be in different ranges (different sessions), but they come back as the same range too.
- Conversely, two timestamps on different calendar weekdays that I know are both inside the same single weekly session sometimes report correctly and sometimes not — it depends on which side of midnight Sunday each one lands on, not which side of the actual 17:00 cutover.

The pattern that's giving me wrong answers is: the comparison appears to be bucketing timestamps by **calendar week** (i.e. by which Sunday–Saturday they belong to), not by which actual session — the one that starts at `StartDay` + `StartTime` and ends a full week later — they fall into. When `StartDay == EndDay`, those two buckets aren't the same thing: a calendar week boundary is at midnight on Sunday, but the session boundary is at the configured time on Sunday.

I'd expect `isInSameRange` to honor the configured `StartTime` on `StartDay` as the actual weekly cutover. The existing case where `StartDay != EndDay` looks fine — it's only this same-day weekly configuration that's broken.

(Setup: Linux, default UTC, no LocalTime override.)
