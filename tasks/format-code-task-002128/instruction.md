# Problem Statement

I'm working with OpenTelemetry tracing in Ruby and I want to attach some array values as span attributes — like a list of tags or a set of numeric IDs related to an operation. Right now whenever I pass an array as an attribute value it just silently disappears and never shows up on the span. Ideally I'd like to be able to set things like `attributes: { "http.status_codes" => [200, 404] }` and have them actually recorded, and I'm also exporting to Jaeger so it'd be great if they come through there in some usable form too.

# Expected outcomes

- Array-valued attributes are accepted anywhere trace attributes are accepted for spans, span events, links, and sampler results, as long as the array elements are all supported attribute scalar values of a compatible type: strings, numerics, or booleans.
- Empty arrays are treated as valid attribute values and are preserved rather than dropped.
- Invalid array-valued attributes, including arrays with unsupported element values or incompatible mixed element types, are rejected consistently with other invalid attributes and do not get recorded.
- Existing scalar attribute behavior for strings, numerics, and booleans remains unchanged.
- When spans or events containing valid array-valued attributes are exported through the Jaeger exporter, those array values are represented in a usable string form that round-trips as JSON for the original array contents.

# Implementation notes

The specific validation structure, helper methods, and where validation is performed are up to the implementer. Preserve the existing public API shape and existing behavior for non-array attributes while extending attribute handling to cover the array cases above.
