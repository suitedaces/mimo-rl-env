## Remove the temporary support-access window from the Support Access settings

In **Settings → Security & Privacy → Support Access**, the panel currently exposes two controls:

1. A toggle to allow Sentry employees to access the organization.
2. A datetime picker that opens a *temporary* access window (Sentry employees gain access until the chosen date/time, then it automatically closes).

We've decided to drop the temporary-window concept. Going forward the only way to grant Sentry employees access to an organization should be the on/off toggle — there is no "open access for the next N hours/days" flow anymore.

### What the panel should look like after this change

- Only the allow-access toggle remains.
- The info banner at the top of the panel reflects the current state of that toggle in two states only:
  - employees currently have access, or
  - employees do not have access.
- No datetime picker, no "until [date]" wording, no "disable permanent access first to set temporary access" affordances — that whole second control is gone.

### Cleanup

The temporary-window feature was the only consumer of the org-level data-secrecy endpoint that this component talked to, plus a chunk of local state (current waiver, formatted date string), an effect that hydrates the picker from the server, and a small date-formatting helper used only by the "until [date]" banner. None of that is needed once the picker is gone — please remove the now-dead code paths and any imports/dependencies that are only there to support them, so the component is just the simple toggle + status banner.

The existing permission gating on the remaining toggle (org:write to modify) should keep working exactly as it does today.
