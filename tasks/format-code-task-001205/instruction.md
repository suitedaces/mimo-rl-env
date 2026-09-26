## Slack webhook notifier doesn't actually send anything

I'm trying to get Slack notifications working for Forseti violations. I added the slack webhook entry to my notifier config with a valid `webhook_url` (verified it works — I can `curl` it from the same host and a message shows up in the channel). When forseti runs and produces violations, no message ever arrives in Slack.

Looking at the notifier logs, the Slack notifier blows up as soon as it tries to run — it never gets as far as POSTing anything. Other notifiers configured in the same run (e.g. email) work fine on the same violations, so the violations are definitely being produced and dispatched; it's just the Slack one that's broken.

Could someone take a look at the slack webhook notifier? Right now it seems completely non-functional — any forseti install that turns it on just silently gets no Slack messages.
