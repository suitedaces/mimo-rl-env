## Feature request: prefix every log message with a static string

I'm using pino across a few subsystems of my app (HTTP layer, a background worker, a proxy module) and I want every log line coming out of a given logger to be visually tagged with the subsystem it came from, e.g.

```
[HTTP] got new request!
[HTTP] user authenticated
```

The natural place to put that tag is at the start of the message itself, so that human-readable consumers (pino-pretty, grep, tailing the file) can immediately see which subsystem produced each line without having to inspect the JSON structure.

Today there doesn't seem to be a clean way to do this. The options I've considered all have downsides:

- Manually prepending the prefix at every call site (`logger.info('[HTTP] got new request')`) — tedious and error-prone, and every developer on the team has to remember to do it.
- Using `child({ component: 'HTTP' })` and reading `component` downstream — works, but it adds a JSON field instead of decorating the human-visible message, and it doesn't help when reading raw log output.
- Wrapping the logger — loses pino's level methods / child / typings.

It would be great if pino supported a first-class option to declare "every message logged through this instance should be prefixed with string X". Something I could pass at construction:

```js
const logger = pino({ /* ... prefix option ... */ })
logger.info('got new request!')
// [HTTP] got new request!
```

A few behaviors I'd expect from such an option, based on how I want to use it:

1. It applies to all log levels uniformly.
2. Children created via `logger.child(...)` inherit it by default — a child of an `[HTTP]` logger should still produce `[HTTP] ...` lines without me having to re-declare anything.
3. I can override / extend it on a child when I want sub-tagging, e.g. an HTTP logger spawning a Proxy child so that proxy lines come out clearly nested under the HTTP context.
4. It only affects the message string. Object logging, bindings, serializers, redaction etc. should behave exactly as today.
5. If I don't set the option, pino behaves exactly as today (no surprise prefix, no perf regression on the hot logging path for users who don't opt in).

This was originally raised in #544. Would the maintainers be open to adding this? A name like `msgPrefix` (accepted both on the top-level `pino({...})` options and as part of the second argument to `.child({}, {...})`) would feel natural.
