## `network_watcher_enabled` check crashes on Azure tenants with multiple subscriptions

When I run prowler against an Azure tenant that has more than one subscription, the `network_watcher_enabled` check blows up instead of producing findings.

Repro:

```
prowler azure --checks network_watcher_enabled
```

Other Azure checks for the same subscriptions complete fine and produce normal PASS/FAIL findings, so credentials and subscription discovery are working. It's specifically this check that errors out partway through and never reports whether Network Watcher is enabled for the locations in my subscriptions.

I'd expect the check to iterate over each subscription, compare the locations that have a Network Watcher against the full list of locations for that subscription, and emit a PASS/FAIL like the other Azure checks do — not crash.
