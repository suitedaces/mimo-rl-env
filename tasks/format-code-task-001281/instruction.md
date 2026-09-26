## Feature request: ISO 8601 duration output from `formatDuration`

`sentry/utils/duration/formatDuration` currently supports a handful of human-facing styles (`count`, `count-locale`, `h:mm:ss`, `hh:mm:ss.sss`, etc). All of them produce text that's meant to be read by a person.

I'd like to render durations inside a semantic `<time>` element so screen readers and other tools can parse them, e.g.

```tsx
<time dateTime={/* machine-readable duration here */}>
  {formatDuration({duration, precision, style: 'h:mm:ss'})}
</time>
```

The `dateTime` attribute on `<time>` expects an ISO 8601 duration string (the format described at https://en.wikipedia.org/wiki/ISO_8601#Durations and https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#durations), and none of the existing `style` options produce that. Right now I either have to write a separate one-off helper or just drop the `dateTime` attribute, which defeats the purpose.

It would be great if `formatDuration` itself grew a `style` option that emits an ISO 8601 duration, so the same function can serve both the visible label and the `dateTime` attribute, and the existing `precision` argument keeps its meaning (asking for `hour` precision shouldn't include minutes/seconds in the output, asking for `ms` precision should keep sub-second detail, etc.).

A name like `'ISO8601'` for the new `style` would feel natural.
