## Problem Statement

Could we make Generate actually validate the output against the schema I pass in the request? Right now I give it an output schema but it'll happily return stuff that doesn't match it, so I'd love for it to just error out when the response doesn't conform instead of silently passing it through.

Also, on the Part side, can I get the fields exposed directly so I can read things like Text and ContentType straight off the struct? Working through the accessor methods makes it awkward to build/inspect Parts and to serialize them properly. And a NewJSONPart helper for constructing JSON content parts would be handy too.

## Expected outcomes

- Generate output schema validation:
  - `ai.Generate` should validate JSON-format generated output against the output schema supplied on the request.
  - When generated output does not conform to the supplied schema, `ai.Generate` should return an error instead of returning the non-conforming response as successful.
  - Generated output that does conform to the supplied schema should continue to be returned successfully.

- Part construction and direct field access:
  - `ai.Part` should expose its kind, content type, text, tool request, and tool response data through exported fields so callers can inspect and serialize parts directly.
  - The exported part kind type and constants should be available for callers that need to construct or inspect parts by kind.
  - Existing part constructors should populate the exported fields consistently with the kind of part they create.
  - `ai.NewTextPart` should create a text part whose `ContentType` field is populated with the plain-text content type value `"plain/text"`.
  - `ai.NewJSONPart` should be available for constructing JSON content parts and should create a text part with JSON content type.

## Implementation notes

- The exact validation location and internal helper structure are up to the implementation, as long as the public `Generate` behavior is correct.
- The exact internal representation of parts may be changed as needed, but callers should be able to use the exported API described above without relying on private accessor methods.
- Preserve existing successful generation and part serialization behavior except where it must change to support direct fields, JSON part construction, and schema-conformance errors.

## Required public API surface (mechanical binding)

The following names / signatures MUST be implemented exactly as listed; downstream Go tests mechanically bind these:

- `ai.Part.Kind ai.PartKind` - exported field for direct part-kind inspection.
- `ai.Part.ToolRequest *ai.ToolRequest` - exported field for direct tool request inspection.
- `ai.Part.ToolResponse *ai.ToolResponse` - exported field for direct tool response inspection.
- `type ai.PartKind` - exported part-kind type; the underlying representation is not specified.
- `ai.PartText`, `ai.PartMedia`, `ai.PartData`, `ai.PartToolRequest`, and `ai.PartToolResponse` - exported kind constants used consistently with the corresponding part constructors and `Is*` methods.
