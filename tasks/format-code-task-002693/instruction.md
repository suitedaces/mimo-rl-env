## Code monitoring usage stats: missing a top-level "monitors enabled" count

When looking at the code monitoring usage statistics that we collect (the
ones produced by `GetCodeMonitoringUsageStatistics` /
`code_monitoring_usage_stats.sql`), I can see counts broken down per action
type — how many email actions are enabled, how many Slack webhook actions
are enabled, how many webhook actions are enabled, plus their unique user
counts.

What's missing is a single aggregate "how many enabled monitor actions are
there in total across the instance" number. Right now, to answer that
basic question from the usage stats payload, a consumer has to grab the
three per-type enabled counts and sum them up themselves (and remember to
treat nulls as zero, since each of those is `NULLIF(..., 0)`-wrapped).

This is the most obvious headline number for code monitoring adoption —
"how many monitors are actually turned on right now" — so it would be much
nicer if the usage stats struct surfaced it directly alongside the existing
per-type counts, instead of every consumer recomputing it.

Could we add this aggregate to `CodeMonitoringUsageStatistics` and have the
SQL query populate it? The new field would be something like `MonitorsEnabled`.
