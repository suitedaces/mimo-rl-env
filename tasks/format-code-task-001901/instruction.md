## Problem Statement

I'm trying to connect with Apollo `subscriptions-transport-ws` using the `graphql-ws` subprotocol, but the browser immediately drops the API Gateway WebSocket connection during `$connect` with a subprotocol negotiation error; in devtools I can see the request sends `Sec-WebSocket-Protocol: graphql-ws`, and the handshake response doesn't include a subprotocol.

## Expected Outcomes

- WebSocket `$connect` responses include a `Sec-WebSocket-Protocol` response header when the client handshake request includes `Sec-WebSocket-Protocol`.
- The response preserves the client-requested subprotocol value so clients using `graphql-ws` can complete WebSocket subprotocol negotiation.
- If the platform exposes the request header as a single value or as header values, the `$connect` response still reflects the requested subprotocol instead of dropping it.
- Requests that do not include `Sec-WebSocket-Protocol` continue to connect successfully without inventing a subprotocol response.
- Existing connection authorization and normal connect/disconnect behavior remain unchanged.

## Implementation Notes

The exact location of the fix, data structures used to read request headers, and how the response is assembled are up to the implementer. The behavior should be validated through the public WebSocket `$connect` handshake response rather than by relying on internal implementation details.
