# Add a machine-readable JSON view to the zpages trace endpoints

The zpages exporter serves two debugging pages over HTTP: `/tracez` (a summary of
collected spans, grouped by span name) and `/traceconfigz` (the current trace
sampling configuration). Today both endpoints only render HTML, which makes them
hard to consume programmatically (for example, from tests or external tooling).

Add an opt-in JSON view to both endpoints, selected with the query parameter
`json=1`. When that parameter is present the endpoint must respond with the same
information it would have rendered as HTML, but serialized as a JSON document
(HTTP 200). When the parameter is absent (or anything other than `1`), the
endpoints keep serving their existing HTML pages unchanged.

## `/tracez?json=1`

Responds with a JSON object describing the per-span-name summary. It has two
fields:

- `spanCells`: an array with one entry per span name currently known to the
  exporter, **ordered ascending by name**. Each entry reports the aggregate
  counts for that name and contains at least:
  - `name`: the span name.
  - `RUNNING`: how many spans with that name have started but not yet ended.
  - `ERRORS`: how many spans with that name finished with a non-OK status (a
    status code other than `0`).
  - `latencies`: an object that buckets the *completed, OK* spans by their
    duration. It has one numeric counter per latency bucket, keyed by these
    exact bucket names: `ZERO_MICROSx10`, `MICROSx10_MICROSx100`,
    `MICROSx100_MILLIx1`, `MILLIx1_MILLIx10`, `MILLIx10_MILLIx100`,
    `MILLIx100_SECONDx1`, `SECONDx1_SECONDx10`, `SECONDx10_SECONDx100`,
    `SECONDx100_MAX`. Every completed OK span lands in exactly one bucket, so the
    sum of the counters equals the number of completed OK spans for that name.

- `selectedTraces`: details about an individual span name selected with the
  `tracename` query parameter, filtered by the `type` query parameter (the same
  parameters the HTML page already understands; `type` may be `RUNNING`,
  `ERRORS`, or one of the latency bucket names). When `tracename` is **not**
  provided this field is `null`. When it is provided, the field is an object
  with:
  - `name`: the requested span name.
  - `traces`: an array of the matching spans. Note that spans contain circular
    references, so they cannot be serialized directly — each entry must be a
    plain, JSON-safe representation that still carries the span's identifying
    information, including its `traceId` and span `id`.

## `/traceconfigz?json=1`

Responds with a JSON object describing the sampling configuration:

- `samplingProbability`: the sampling probability currently in effect on the
  tracer (e.g. `1` when sampling is always on, `0` when it is never on).
- `defaultConfig`: an object whose `samplingRate` is a number.

The HTML responses, and any existing behavior of these endpoints when `json=1`
is not supplied, must continue to work exactly as before.
