## Problem Statement

Right now I can only point YACE at the standard AWS service namespaces through discovery and static jobs, but I'm publishing my own custom metrics to CloudWatch (like host CPU and disk stats under my own namespace) and there's no way to scrape those. Could you add a way for me to define jobs against arbitrary CloudWatch namespaces — basically let me specify the namespace, which regions/roles to use, and the list of metrics I want pulled? Ideally the exported Prometheus metrics would keep whatever CloudWatch dimensions those metrics have as labels too. It'd also be nice if metrics with no data points just got skipped instead of showing up as empty series.

## Expected outcomes

- Custom CloudWatch metric jobs can be declared in configuration through a top-level `customMetrics` YAML key, and the public configuration model exposes these jobs via `ScrapeConf.CustomMetrics` / `CustomMetrics`.
- Each custom metric job can describe its job name, CloudWatch namespace, regions, roles, metrics, and the same per-metric defaults used by existing metric definitions where applicable, including statistics, nil-to-zero behavior, period, length, delay, and CloudWatch timestamp handling.
- A configuration containing only valid custom metric jobs is accepted as a non-empty scrape configuration.
- When roles are not provided for a custom metric job, the exporter treats it as using the current AWS identity, consistent with existing job types.
- During scraping, custom metric jobs are processed for their configured role and region combinations, and matching metrics from the configured CloudWatch namespace are collected and exported as Prometheus metrics.
- Exported custom namespace metrics preserve the CloudWatch dimensions associated with each metric as Prometheus labels.
- Custom namespace metrics whose CloudWatch query returns no data points are skipped rather than emitted as empty series.
- User-facing documentation describes the custom metric configuration capability and includes enough information to configure it.

## Implementation notes

- The internal structure, concurrency strategy, helper functions, and exact validation plumbing are up to the implementer.
- Preserve existing discovery and static job behavior while adding support for custom CloudWatch namespaces.
- Tests should validate externally observable configuration, scraping, exported metric, and documentation behavior rather than relying on a particular internal helper layout.
