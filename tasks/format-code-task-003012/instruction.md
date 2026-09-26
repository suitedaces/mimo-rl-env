## SetJiraServiceOptions is missing event-toggle fields, can't tame Jira notification spam from the SDK

I'm using `ServicesService.SetJiraService` to configure the Jira integration across a bunch of projects programmatically. The Jira side ends up extremely noisy — every push, every MR update, every comment seems to fire something into Jira. In the GitLab web UI for the Jira service there are checkboxes to control which events actually trigger the integration, and the GitLab services REST API documents the corresponding boolean fields too.

The problem is that `SetJiraServiceOptions` (and `JiraServiceProperties` on the read side) in this library only exposes the connection-level fields — URL, project key, username/password, the issue transition id. None of the event-toggle fields the API supports are there, so from go-gitlab there's no way for me to turn off the noisy event types when I provision projects. I either have to accept the spam or click through the UI on every project, which defeats the point of using the SDK.

For comparison, lots of the other service options in `services.go` (Slack, Custom Issue Tracker, etc.) already expose this kind of `*_events` boolean, and the base `Service` struct itself has a bunch of these event flags — Jira just got left behind.

Could the Jira service options/properties be brought in line with what the GitLab API actually supports for that integration so the event triggers can be toggled from code? In particular the comment-toggle one in the GitLab API isn't named like a plain `*_events` flag — it's something like `CommentOnEventEnabled` — so please use that name (and the matching JSON tag) rather than inventing a `CommentEvents`.
