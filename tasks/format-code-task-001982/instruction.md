### Describe the problem and steps to reproduce it:
The weekly content reviewer report wasn't sent out, because the display name for a user was `None`.

### What happened?

https://sentry.prod.mozaws.net/operations/olympia-prod/issues/5140376/?query=is:unresolved

### What did you expect to happen?

Should use `Firefox user {user-id}` if `display_name` is `None`.

### Anything else we should know?
(Please include a link to the page, screenshots and any relevant files.)

Deleted users should not show up on the weekly reviewer report.
