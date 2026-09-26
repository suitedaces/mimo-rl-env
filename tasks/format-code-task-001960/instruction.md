## `onLog` callback in compass-web exposes raw internal logger arguments instead of a processed log event

We're embedding `compass-web` and wiring up the `onLog` callback on the React component so that we can pipe Compass's internal logs into our own logging/observability pipeline (the same one that already ingests structured log lines from the desktop Compass app, which uses `mongodb-log-writer`).

The problem is that the shape of what `onLog` receives is not really a usable log entry — it's basically the raw arguments that were passed into the internal log writer:

```ts
onLog: (type, ...args) => {
  // type is 'debug' | 'info' | 'warn' | ...
  // args is whatever the caller happened to pass in — component name,
  // a message id, a message string, an attr object, in no particular
  // consistent shape.
  myLogSink.write({ /* ??? how do I turn this into a real log record ??? */ });
}
```

A few things make this awkward in practice:

- There's no timestamp on what we receive, so we have to stamp it ourselves at the moment the callback fires, which isn't necessarily when the log event was actually produced.
- We don't get a stable, structured object — just positional args — so we can't reliably extract the component, the message id, the message text, or the attached attributes without making assumptions about argument order.
- The shape is completely different from what Compass desktop produces via `mongodb-log-writer`. We already have tooling that consumes that JSON-per-line format; we'd like to reuse it as-is for compass-web logs, but right now we'd have to write a separate adapter just for the web embed.

It also feels like a leaky abstraction — the consumer of `<CompassWeb onLog={...}>` shouldn't really need to know how the internal log writer is called in order to make sense of a log entry.

Could `onLog` instead hand us a single processed log event object, with the same structure that Compass produces elsewhere through its log writer (timestamp, severity, component, message id, message, optional attributes)? That way embedders can just forward whatever `onLog` gives them into their existing log pipeline without having to reconstruct a log record from positional arguments.
