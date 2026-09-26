## Publishing a keepalive event via the HTTP API has no effect on the entity

I have a proxy entity that isn't backed by a running agent, but I'd still like to "ping" it periodically from an external script so it shows up as recently seen. The natural way to do this seems to be POSTing/PUTting a keepalive event to the events HTTP API.

Before:

```
$ sensuctl entity list
   ID    Class    OS     Subscriptions             Last Seen
 ────── ─────── ─────── ─────────────── ───────────────────────────────
  cube   agent   linux   entity:cube     2020-03-05 15:46:07 -0800 PST
  me     proxy           test            N/A
```

Then I publish a keepalive-shaped event for `me`:

```
curl -X PUT -H 'Authorization: Key <redacted>' \
     --data @keepalive.json \
     -H 'Content-Type: application/json' \
     http://localhost:8080/api/core/v2/namespaces/default/events/me/keepalive
```

The request comes back with no error, but the entity's last-seen time never updates:

```
$ sensuctl entity list
   ID    Class    OS     Subscriptions             Last Seen
 ────── ─────── ─────── ─────────────── ───────────────────────────────
  cube   agent   linux   entity:cube     2020-03-05 15:46:07 -0800 PST
  me     proxy           test            N/A
```

If I send the exact same payload from an actual agent's keepalive mechanism, the entity's last-seen updates as expected — so the data shape is fine, it just seems that keepalive events submitted through the HTTP events API don't get treated like keepalives at all.

It would be very useful to be able to publish keepalives via the HTTP API (same endpoint as other events, using `keepalive` as the check name), so that external tooling can keep proxy entities alive without having to run a full agent.
