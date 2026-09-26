## Re-POSTing to a toxic endpoint wipes out fields I didn't include in the body

I'm using toxiproxy's HTTP API to manage a latency toxic on one of my proxies from a script. First I configure it with the full set of values:

```
POST /proxies/myproxy/upstream/toxics/latency
{"enabled": true, "latency": 1000, "jitter": 100}
```

Later in the same script I want to temporarily disable it, so I send just the field I'm changing:

```
POST /proxies/myproxy/upstream/toxics/latency
{"enabled": false}
```

After the second POST, if I `GET /proxies/myproxy/upstream/toxics` I can see that `latency` and `jitter` have both been reset to `0`. So even though I only sent `enabled` in the body, the rest of the toxic's configuration got blown away.

That feels wrong — I'd expect POSTing to a toxic that's already been configured to behave like a partial update: whatever fields I send in the body get updated, and anything I omit keeps whatever value it had before. Otherwise every time I want to tweak one knob (e.g. toggle `enabled`) I have to re-send the entire configuration, and any client that doesn't remember the previous values can silently clobber them.

Same thing happens on the downstream endpoint. Could the toxic update preserve previously-set fields when the request body only contains a subset of them?
