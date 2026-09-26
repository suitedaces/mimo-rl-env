## Make the filter for the homepage graph configurable

The big graph at the top of the console home page (the one showing Gbps over time) only shows flows where the input interface boundary is `external`. That criterion is baked into the query and I can't find any way to change it from the configuration.

This is awkward in a couple of deployments I'm running:

- One instance is on a network where I haven't bothered classifying interfaces as external/internal — everything stays `undefined`. The homepage graph is just flat at zero even though the per-source-AS / per-country widgets right below it clearly show traffic going through. New users land on the page and assume Akvorado isn't actually receiving anything.
- Another instance is used purely for internal observability inside a single AS. There's no "edge" in any meaningful sense and I'd much rather have that graph show the sum of *all* captured flows than nothing at all.
- And in general, "edge ingress" isn't always the most useful default — depending on the deployment I might want to filter on a different boundary, a specific exporter group, etc.

It would be great if this could be exposed in the console configuration alongside the existing keys like `homepage-top-widgets`, `dimensions-limit` and `cache-ttl`, so each operator can pick whatever criterion makes sense for their setup — including no extra filter at all (i.e. just sum everything). The current behaviour should remain the default so existing deployments don't suddenly start showing different numbers.

A natural name for the new console config key would be something like `homepage-graph-filter`.
