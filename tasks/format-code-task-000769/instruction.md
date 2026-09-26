I'm trying to trace exactly which version of a dbt node ran just from the structured log events, but `node_info` doesn't tell me the node's source checksum, so I have to go look it up somewhere else. Could dbt include the node checksum in the `node_info` event data when it's available?

Expected outcomes:
- Structured log event data that includes `node_info` should expose a `node_info.node_checksum` field.
- When the logged node has a source checksum available, `node_info.node_checksum` should contain that checksum string so log consumers can identify the exact node source version from the log event alone.
- When the logged node does not have checksum information available, `node_info.node_checksum` should still be present in the Python dictionary representation and should have a null/`None` value rather than a source hash.
- The protobuf event contract should expose the same information through `NodeInfo.node_checksum`.

Implementation notes:
- The specific code path, data structure, and validation location used to populate the checksum are up to the implementer, as long as the existing structured logging behavior is preserved and the checksum is consistently represented in both the dictionary event data and the protobuf event data.
