## Feature request: allow external metric rules to opt out of HPA-namespace scoping

I'm using prometheus-adapter to expose some external metrics for HPAs. My use case is pretty common: I have a workload (a Deployment + HPA) in one namespace that needs to scale based on a metric coming from a service that lives in a *different* namespace.

Concrete example: I have an NSQ deployment in a `nsq` namespace which exposes `nsq_topic_depth` for each topic. I have a worker Deployment in the `default` namespace whose HPA should scale on the depth of one of those topics.

I configure an external rule something like:

```yaml
externalRules:
- seriesQuery: 'nsq_topic_depth'
  metricsQuery: sum(<<.Series>>{<<.LabelMatchers>>}) by (topic)
  resources:
    overrides: { namespace: { resource: "namespace" } }
```

and an HPA in `default`:

```yaml
- type: External
  external:
    metric:
      name: nsq_topic_depth
      selector:
        matchLabels:
          topic: my-topic
          namespace: nsq
```

The problem is that the adapter always tacks the HPA's own namespace onto the generated Prometheus query as a label matcher. So even though my selector explicitly says `namespace: nsq`, the resulting query ends up filtering on `namespace="default"` (the HPA's namespace) and returns nothing — the metric series simply does not exist in `default`.

As far as I can tell there is currently no way to tell the adapter "this external metric isn't tied to the HPA's namespace, please don't add that label filter for me." The auto-injected namespace makes sense for in-cluster resource-bound metrics, but for external metrics coming from a third service it's actively in the way: I can't query a different namespace, and I can't query metrics that have no `namespace` label at all.

Would it be possible to add a way to declare, per external rule, that the metric is not namespace-scoped, so the adapter leaves the namespace alone and lets the HPA's metric selector decide whether/which namespace label to set? Existing rules should keep their current behavior (namespace is auto-added) so this doesn't break anyone.

I'd expect this to surface at the metrics-query builder layer too — e.g. something like a dedicated `NewExternalMetricsQuery(..., namespaced bool)` constructor so the namespace-injection behavior can be toggled per external rule.
