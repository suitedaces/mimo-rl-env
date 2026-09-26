# Carry the original connection ID in the transport parameters

When a QUIC server answers a client's first Initial with a Retry, it forces the
client onto a new connection ID. To let the client authenticate that Retry, the
server has to echo back the destination connection ID the client originally
used. That value travels inside the handshake's transport parameters, but our
`TransportParameters` type has no notion of it yet.

Add support for an *original connection ID* transport parameter.

Requirements:

- `TransportParameters` must expose an exported field `OriginalConnectionID` of
  type `protocol.ConnectionID` that holds this value.

- The value must take part in the on-the-wire encoding of the transport
  parameters. When it is set, serializing a `TransportParameters` and then
  parsing the produced bytes again must recover exactly the same connection ID.
  When it is not set, the encoding must stay byte-for-byte what it was before
  (no parameter emitted).

- Only a server is allowed to send this parameter. When transport parameters
  that were sent *by a client* are parsed and they contain an original
  connection ID, parsing must fail with an error that names the offending
  parameter (the message must mention `original_connection_id`). Transport
  parameters sent by a server that contain it must parse successfully.

- The human-readable string representation of `TransportParameters` must include
  the original connection ID when one is present, and must be left exactly as it
  was when it is absent.
