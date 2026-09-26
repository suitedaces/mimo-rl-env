## Feature request: support Kafka static membership to avoid rebalances on worker restart

We run a Faust app with several worker instances in the same consumer group. Whenever we do a rolling deploy (or any single instance restarts briefly), the whole group goes through a rebalance — every other worker pauses processing while partitions get reshuffled, and then most of them get the same partitions back anyway. For a fleet of any size this is a significant interruption on every deploy.

Kafka 2.3+ has a "static membership" protocol that's designed exactly for this: if a consumer is configured with a stable group instance id and it goes away and comes back within the session timeout, the broker keeps its assignment and skips the rebalance. The other workers in the group never notice. The underlying `aiokafka` client supports this, but as far as I can tell there's no way to opt into it from the Faust side — Faust never tells aiokafka that a consumer has a stable identity, so we always get the dynamic-membership behavior.

It would be great if Faust's app config exposed this so we could give each worker instance a stable id (e.g. derived from the pod/host name in our deployment), and Faust would propagate that down to the Kafka consumer. When it's not configured, behavior should be unchanged from today (dynamic membership, default rebalance on every restart).

The user-visible behavior we're after:

- Configure a stable per-instance id on each worker.
- Restarting one worker (within `broker_session_timeout`) does not trigger a rebalance for the rest of the group; the restarted worker comes back up and resumes its previous partitions.
- Leaving the new option unset preserves the current behavior.

I'd expect this to live on `app.conf` as a new setting, something like `consumer_group_instance_id`.
