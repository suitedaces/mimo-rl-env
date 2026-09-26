# Problem Statement

I’m seeing our vsrpc endpoint fall over when one of my RPC methods hits a panic — the client just gets a dropped/hung connection instead of a normal JSON-RPC failure for that call. It’s also awkward to verify because the debug service doesn’t seem to have a simple RPC method I can call that deliberately panics with a message.

# Expected outcomes

- Panic handling for vsrpc calls
  - If a vsrpc RPC method panics while handling a request, that panic should be reported to the caller as a JSON-RPC error for that request instead of causing the endpoint, process, or connection to fail.
  - After one RPC call panics and returns an error, the same server/connection should remain usable for subsequent RPC calls.
  - This behavior should apply consistently to RPC methods adapted through the existing vsrpc handler helper APIs, whether the method returns only an error or returns a value plus an error.

- Error details
  - The JSON-RPC error for a recovered panic should use `jsonrpc2.InternalError`.
  - The error message should start with `panic:`, include the panic value, and include stack trace information.

- Debug service verification
  - The debug service should expose a callable vsrpc method named `TestPanicAsync`.
  - Calling `TestPanicAsync` with a message should deliberately trigger the panic path and return the same JSON-RPC internal error behavior, including the supplied message in the error details.

# Implementation notes

The specific recovery mechanism, helper structure, and placement of validation or error conversion are left to the implementer. Preserve the existing request unmarshalling, cancellation, and normal success/error behavior for non-panicking calls.
