## Support `scheduling_options` / cumulative evaluation window on `DatadogMonitor`

I'm using the operator to manage monitors via GitOps. I'd like to set up a few "calendar-aligned" cumulative monitors — e.g. a monthly cost / usage budget alert that resets on the 1st of each month, and a daily SLO-like accumulator that resets at 00:00 UTC.

In the Datadog UI (and via the public Datadog API) this is exposed through `scheduling_options.evaluation_window`, where you can pick a cumulative window aligned to the start of the hour, day, or month (`hour_starts` / `day_starts` / `month_starts`). The behaviour is different from a rolling timeframe — values accumulate from the alignment point instead of sliding.

The problem is I don't see any way to express this on a `DatadogMonitor` CR. `spec.options` covers a lot of the usual stuff (`timeoutH`, `requireFullWindow`, `notificationPresetName`, thresholds, renotify settings, etc.) but there's no field for the evaluation window / scheduling options. If I add it under `spec.options` anyway, the K8s API server rejects it as an unknown field, and even if I bypass that the controller has no logic to forward it to the Datadog API — the resulting monitor in Datadog ends up with the default rolling window instead of the cumulative one I asked for.

For folks managing budget / quota style monitors as code, this means we currently have to click those monitors together in the UI (or maintain them through a separate Terraform pipeline) instead of keeping them next to the rest of our `DatadogMonitor` manifests.

Could the operator expose the scheduling options / cumulative evaluation window on `DatadogMonitor` so it reaches parity with the Datadog API? All three alignment kinds (hourly / daily / monthly) should be configurable, and the controller should pass them through when creating / updating the monitor.
