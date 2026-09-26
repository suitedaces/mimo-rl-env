MCP Inspector sends empty arrays/objects for optional parameters instead of omitting them
MCP Inspector automatically sends empty arrays [] for optional array parameters instead of omitting
   them from tool call arguments, causing issues with OpenAPI servers that expect optional parameters
   to be completely absent when not specified.

##  To Reproduce

  Steps to reproduce the behavior:
  1. Connect MCP Inspector to an OpenAPI server with optional array parameters (e.g., fields[mesh],
  include)
  2. Call a tool without specifying values for optional array parameters
  3. Observe that Inspector sends empty arrays [] instead of omitting the parameters
  4. Check server logs to see the received arguments contain "parameter_name": []

##  Expected behavior
  When optional array parameters are not specified by the user, they should be completely omitted
  from the tool call arguments JSON, not sent as empty arrays. According to MCP best practices:
  - Parameter should NOT be assigned a default value
  - Parameter should NOT be sent as null or []
  - Parameter should be completely absent from the request

##  Logs

  Server receives tool call arguments with unwanted empty arrays:

```json
  {
    "mesh_id": "urn:gltf-live:mesh:0198e08e-8b97-7950-9822-347f217b628e",
    "fields_mesh": [],
    "include": [],
    "timeout_seconds": 30
  }
```

##  Additional context

  - Root cause is in [https://github.com/modelcontextprotocol/inspector/blob/0ef91d229509120521aac8942181b5843bfc45e5/client/src/utils/schemaUtils.ts#L111-L114](https://github.com/modelcontextprotocol/inspector/blob/0ef91d229509120521aac8942181b5843bfc45e5/client/src/utils/schemaUtils.ts#L111-L114) where `generateDefaultValue` returns `[]` for
  optional arrays or `{}` for optional objects
  - A similar issue was previously fixed:
  https://github.com/modelcontextprotocol/inspector/pull/357
  - The fix should update the function to return `undefined`
