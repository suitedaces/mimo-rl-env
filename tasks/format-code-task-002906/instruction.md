## Make the `host` tag on emitted metrics optional, and drop the unused logger metrics

We're running into two related metrics concerns with zanzibar:

### 1. `host` tag is always attached to every metric

Right now every metric the gateway emits ends up with a `host` tag (the hostname of the machine running the process). For a large fleet this blows up the cardinality of every single series we emit — call metrics, circuit breaker metrics, custom counters, everything. In our metrics backend that's expensive and most of the time we don't actually want per-host breakdowns for application-level metrics; we already have other ways to get per-host visibility.

There is currently no way to turn this off without forking — the host tag is just unconditionally added in the gateway's metrics setup.

What we'd like:

- A way (via static config) to opt out of attaching the `host` tag to the gateway's metrics.
- Runtime metrics (GC, mem, CPU, goroutine counts, etc.) should keep being emitted with a `host` tag regardless of that setting, because those metrics are only useful when you can attribute them back to a specific host. So the toggle should apply to "regular" metrics, not runtime ones.

This will be a breaking change for anyone relying on the current behavior, which is fine — we'd just like the knob to exist and be required so people make a conscious choice.

### 2. `zap.logged.<level>` counters aren't really useful

The gateway wraps its zap core so that every log line increments a per-level counter (`zap.logged.debug`, `zap.logged.info`, `zap.logged.warn`, `zap.logged.error`, etc.). In practice nobody is alerting on or looking at these — they're extremely coarse (just "how many log lines did we emit?") and they don't tell you anything you can't get from the logging pipeline itself. Meanwhile they add machinery to the logger setup and to `SubLogger`.

We'd like to just remove these counters and the wrapping core, and have the gateway's logger use a plain zap core directly.

---

Happy to take these as one change or two, but they're both blocking us from cleaning up our metrics dashboards.

(For the config knob, we'd expect the new field to live under the existing `metrics.m3.*` namespace — something like `metrics.m3.includeHost`.)
