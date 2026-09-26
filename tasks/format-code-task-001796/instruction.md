## Metrics tables: split namespace into its own column

When viewing the pod / deployment metrics tables in the dashboard, the resource column shows entries like:

```
emojivoto/web-svc
emojivoto/voting-svc
booksapp/authors
booksapp/webapp
```

i.e. the namespace is glued to the resource name with a `/`. This is awkward for a few reasons:

- I can't sort or scan by namespace independently — everything is bundled into one string column.
- Sorting by "name" actually sorts by namespace first because of the prefix, which isn't what the column header (`Pod` / `Deployment`) suggests.
- It's harder to read at a glance which namespace a row belongs to when there are many resources from a few namespaces mixed together.

It would be much nicer if the metrics table had a dedicated **Namespace** column next to the resource name column, both independently sortable, so the table reads like:

```
Namespace     Pod          Success Rate   Request Rate   ...
booksapp      authors      ...
booksapp      webapp       ...
emojivoto     voting-svc   ...
emojivoto     web-svc      ...
```

A couple of related observations while I'm here:

1. The Grafana link from the resource name still needs to deep-link to the right namespace + resource dashboard, so whatever change is made should keep that working.
2. On the deployments overview page (the status table that shows pod health dots) the resource cell currently shows `namespace/deployment` as one string — that display is fine to keep there, since that page only has a single resource column, but it should still link through to the right Grafana dashboard.
3. The metric columns (`Success Rate`, `Request Rate`, `P50/P95/P99 Latency`) are pretty wide for what they hold (a single number) — once a Namespace column is added the table gets crowded. It'd be nice if the numeric columns were narrower so the name/namespace columns get more room.

Could the metrics table be updated so namespace is a first-class column?
