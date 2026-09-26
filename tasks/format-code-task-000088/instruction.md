## Transaction system migrations trigger more recoveries than necessary

I'm running a FoundationDB cluster managed by the operator and recently did
a configuration change that touches multiple transaction system process
classes at once (something that requires replacing both my log and stateless
processes). I expected the whole change to settle with a single recovery at
the end, but I'm seeing more than one recovery during what I'd consider one
migration.

What I can observe from the operator logs and the cluster during this kind
of change:

- The new stateless pods come up pretty quickly because they don't need
  persistent storage.
- The operator excludes the old stateless processes as soon as their
  replacements are ready → a recovery happens.
- The new log pods take noticeably longer because they have to wait for PV
  provisioning.
- Once those are finally up, the operator excludes the old log processes →
  another recovery happens.

So a single config change ends up producing a recovery per transaction
process class as each batch of replacements comes online, instead of one
recovery at the end. Each recovery is disruptive for our workload, and for
a migration that's logically "replace the transaction system", I'd really
only expect one.

Would it be possible for the operator to coordinate exclusions across the
transaction system process classes — i.e. hold off on excluding any of them
until it's ready to make progress on all the affected transaction classes
together — so that this kind of migration converges in a single recovery?
Storage replacements are typically much rarer than transaction-system churn
in our environment, so even just batching the transaction side would help
a lot.
