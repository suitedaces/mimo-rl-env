## Problem Statement

I’m seeing a couple of weird Nightscout display/alert issues: when OpenAPS is `notenacted`, the OpenAPS pill shows “Not Enacted” twice and I don’t see the actual suggestion details there. Also, when I add an active “OpenAPS Offline” treatment, the Pump pill still goes warning/urgent from pump-status health checks and keeps triggering pump alerts.

## Expected outcomes

- OpenAPS pill rendering:
  - When OpenAPS status is `notenacted`, the pill should still show the `notenacted` status, but its detail/info rows should show the suggestion details rather than repeating “Not Enacted” as the detail value.
  - The suggestion details shown for `notenacted` should be consistent with the details shown for other OpenAPS suggestion-present states such as enacted or looping states.

- Pump status and alerts during OpenAPS offline periods:
  - While there is a currently active “OpenAPS Offline” treatment, Pump Status should not be escalated to warning or urgent because of pump-status-derived checks.
  - During that active offline period, pump-related notifications should not be raised solely from those pump status checks.
  - “OpenAPS Offline” treatments that are not currently active should not suppress normal Pump Status warning/urgent behavior.

- Observability:
  - When pump alert checks are skipped because OpenAPS is known to be offline, the system should emit an informational log indicating that alert checks were skipped for that reason.

## Implementation notes

- Preserve the existing Nightscout/OpenAPS data and UI conventions; the exact location of the checks, data structures, and helper organization are up to the implementer.
- Do not disable normal OpenAPS or Pump Status warning/urgent behavior outside an active “OpenAPS Offline” period.
- Keep the change behavior-focused: `notenacted` should display useful suggestion details, and active offline treatments should suppress only the pump-status-derived alert escalation described above.
