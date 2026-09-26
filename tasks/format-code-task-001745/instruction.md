## Problem Statement

Hey, is there any way to actually see what's in the minikube audit log? Right now stuff gets written but I can't find a clean way to pull up, say, the last 10 commands somebody ran on this machine as a readable table — command, profile, user, when it ran, etc. Would be super helpful for debugging when a teammate says "minikube broke" and I want to know what they actually did.

Also while you're in there, could the audit entries include which minikube version was running? Right now I can see the command but not the version it ran under, which makes triaging multi-version setups kind of a pain.

## Expected outcomes

- Audit reporting API:
  - `audit.Report(lastNLines int)` should return an `*audit.RawReport` representing at most the most recent `lastNLines` audit log entries.
  - When more audit entries exist than requested, the report should include the newest entries and omit older ones.
  - Calling `audit.Report` with `lastNLines <= 0` should return no report and an error explaining that the requested line count must be at least 1.
  - A report requested after audit entries have been written in the same process should be able to read those entries back.

- Human-readable report output:
  - `(*audit.RawReport).ASCIITable()` should render the report as a readable ASCII table.
  - The table should include columns for command, args, profile, user, minikube version, start time, and end time.
  - Each included audit entry should appear as one body row with the corresponding values in those columns.

- Audit entry contents:
  - Newly written audit log entries should include the minikube version that was running when the command was logged.
  - Existing audit entry fields such as command, args, profile, user, start time, and end time should continue to be recorded.

## Implementation notes

- The specific internal data structures, parsing strategy, buffering approach, and table-rendering implementation are up to the implementer.
- Preserve the existing audit log append behavior while adding the ability to read back and format recent entries.
- Keep the reporting behavior based on externally observable audit log contents rather than on any particular internal representation.
