# Problem Statement

I'm using python-opcua and I'm running into a modeling issue with audit events. The OPC UA spec lets the emitting node (the one actually firing the event) be different from the SourceNode the event describes — e.g. the Server object emits an AuditCreateSessionEvent whose SourceNode points at the session/session diagnostics node. But with `BaseEvent` and all the `Audit*Event` constructors I can only pass `sourcenode`, there's no way to tell it which node is actually emitting. Could we get a way to specify the emitting node separately when constructing these events, ideally defaulting to the Server object so I don't have to set it every time?

# Expected outcomes

- `BaseEvent` construction supports specifying an emitting node separately from `sourcenode`; when both are provided, the event’s emitting node behavior follows the emitting-node argument while the `SourceNode` event field still reflects `sourcenode`.
- `BaseEvent` construction remains backwards compatible for existing `sourcenode`, `message`, and `severity` usage.
- When no emitting node is provided to `BaseEvent`, the event defaults to being emitted by the OPC UA Server object.
- Public `Audit*Event` constructors support the same emitting-node option and pass it through consistently, so audit event subclasses can be emitted by a node different from the `SourceNode` they describe.
- Public `Audit*Event` constructors keep the same default behavior as `BaseEvent`: omitting the emitting node uses the Server object, and existing `sourcenode`, `message`, and `severity` arguments continue to work.

# Implementation notes

- Preserve the existing public event-construction style while adding the new emitting-node capability.
- The concrete internal representation, validation location, and propagation mechanism are up to the implementation, as long as externally constructed and generated events behave as described.
- Avoid coupling `SourceNode` semantics to the emitting node; callers must be able to set them independently.
