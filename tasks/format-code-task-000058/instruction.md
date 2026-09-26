### Feature request: expose the agent process start time to Python checks

I'm writing a custom Python check and I need to know when the agent process itself started up (i.e. roughly the time the agent was (re)started on the host). Use cases:

- Skipping / filtering out events or log entries from before the agent came up, so a freshly-restarted agent doesn't re-emit old stuff.
- Computing how long the agent has been running, for sanity-check metrics in the check itself.
- Distinguishing "the agent just started, this is the first run" from "the agent has been running for a while" when deciding what state to publish.

From inside a check (Python side), I can get things like the hostname, the cluster name, the agent version, etc. via the `datadog_agent` module, but I can't find anything that tells me when the agent process actually started. As far as I can tell there is no way to get this value from Python today — the agent obviously knows it internally (it has to, for its own status page / flare), it's just not surfaced to checks.

Could the agent expose its process start time through the `datadog_agent` module so checks can read it? A timestamp (seconds since the epoch) would be the most useful shape — that's trivial to compare against `time.time()` from inside a check. Something like `datadog_agent.get_process_start_time()` would be ideal.
