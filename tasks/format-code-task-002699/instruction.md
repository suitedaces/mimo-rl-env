# Dynamic mapping for CI pipeline generation

Spack's CI configuration lets you shape the generated GitLab pipeline through entries under
`ci: pipeline-gen:` — today those are the `submapping` blocks and the various named-job blocks
(`build-job`, `signing-job`, …). For large-scale CI we want to be able to compute job attributes
at generation time by asking an external web service, instead of hard-coding everything in the
config.

Add a new kind of `pipeline-gen` entry, `dynamic-mapping`, that fetches per-job attributes from a
REST endpoint and merges them into the matching build jobs.

## Configuration

A `dynamic-mapping` entry is an object with a single `dynamic-mapping` key whose value supports:

- `endpoint` (string, **required**): the base URL of the mapping service.
- `name` (string, optional): a label for the section.
- `allow` (list of strings, optional): attribute keys that are allowed to be applied.
- `ignore` (list of strings, optional): attribute keys that must never be applied.
- `require` (list of strings, optional): attribute keys that must be present in the (filtered)
  response.
- `header` (object, optional): extra HTTP headers to send with the request.
- `timeout` (non-negative integer, optional) and `verify_ssl` (boolean, optional): request knobs.

No other keys are permitted inside `dynamic-mapping`, and an entry missing `endpoint` is invalid.
A configuration that lists a `dynamic-mapping` entry must validate against the CI schema, while one
that omits the required `endpoint` (or adds an unknown key) must be rejected.

## Behavior during `spack ci generate`

For every job that builds a concrete spec, issue an HTTP GET request to the configured `endpoint`.
The request URL must carry a query string identifying the spec to build — i.e. a `spec` query
parameter whose value describes the spec (package name, version, variants, architecture and
compiler). Named/utility jobs that are not tied to a concrete spec are not queried.

The response body is JSON: an object mapping job-attribute names to values. Before merging it into
the job, filter it as follows:

1. **ignore** — drop every key listed in `ignore`.
2. **allow** — if `allow` is non-empty, keep only keys that appear in `allow`; drop the rest. Keys
   listed in `require` are implicitly allowed even if not present in `allow`. If `allow` is empty or
   absent, keep everything that survived the ignore step.
3. **require** — if any key listed in `require` is missing from the filtered result, emit a warning
   of the form `Response missing required keys: [...]` (listing the missing keys). This is only a
   warning; pipeline generation continues.

Whatever survives filtering is deep-merged into the job's existing attributes (the same merge
semantics used elsewhere for CI config, so e.g. a `variables` object combines with any variables the
job already has). `dynamic-mapping` does not support the `-remove`/override-suffix behavior that
named-job and submapping sections have.

If the request itself fails (connection error, non-success status, unreadable body, …), it must not
abort generation: warn and continue so the rest of the pipeline is still produced.
