# Make trace IDs parseable from hex and span contexts JSON-friendly

Our tracing core can already render a `TraceID` to its 32-character hex string
(via `SpanContext.TraceIDString()`), but there's no way to go the other
direction, and dumping a `SpanContext` to JSON produces something unreadable.

Please add two things to the tracing core.

## 1. Construct a `TraceID` from a hex string

Add an exported constructor in the core tracing package with the signature:

```go
func TraceIDFromHex(h string) (TraceID, error)
```

It parses a [W3C trace-context](https://www.w3.org/TR/trace-context/#trace-id)
compliant trace-id. A string is accepted **only** when all of the following
hold; otherwise it returns a non-nil error:

- it is exactly 32 characters long;
- every character is in `[0-9a-f]` — digits and **lowercase** hex letters only
  (uppercase `A`–`F` is rejected);
- it is not the all-zero id (`"00000000000000000000000000000000"`).

When the input is valid, the returned `TraceID` must be the inverse of the
existing hex formatting: putting it into a span context and calling
`TraceIDString()` must reproduce the original input string exactly. Parsing the
same hex string twice yields equal trace ids, and distinct hex strings yield
distinct trace ids. A freshly parsed (valid) trace id makes
`SpanContext.HasTraceID()` report `true`.

## 2. Human-readable JSON for `SpanContext`

Marshaling a `SpanContext` with `encoding/json` should produce a JSON object
whose trace id and span id appear as their hex string forms rather than as raw
numeric fields. Specifically the object must contain:

- `"TraceID"`: the trace id as its 32-character hex string (same value as
  `TraceIDString()`);
- `"SpanID"`: the span id as its 16-character hex string (same value as
  `SpanIDString()`);
- `"TraceFlags"`: the trace flags as their numeric byte value.
