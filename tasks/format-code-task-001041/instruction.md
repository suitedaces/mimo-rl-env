## Make API request retries safe, complete, and observable

The shared Proxmox API client currently retries only a narrow class of transport failures. That leaves ordinary idempotent operations exposed to transient connection failures, while any expansion of retries must not accidentally duplicate a mutating operation or replay a streaming upload. Please make retry behavior a deliberate part of the client contract so all resource implementations receive the same behavior.

For replayable `GET`, `HEAD`, `PUT`, and `DELETE` requests, retry a transport failure and a transient HTTP response with status `429`, `502`, `503`, or `504`. There must be no more than three total attempts. A successful later attempt must return normally; when all attempts fail, return the final transport or HTTP failure, retaining the normal typed HTTP error and server-detail behavior. Every response body received from an abandoned transient attempt must be closed before the next attempt, and the final response body must still be cleaned up on both success and failure.

Retries must create a fresh request for every attempt. In particular, URL-encoded request data for a replayable request must be sent intact on every attempt, and request authentication must be applied to every freshly created request. Do not retry if the request context has been canceled or if authentication fails while setting up an attempt; return that error without sending another request.

Safety takes precedence over availability. Never retry `POST` or `PATCH`, even when their failure would otherwise be transient. Likewise, never retry a request whose body is a `MultiPartData` stream or an `io.PipeReader`, including when the HTTP method itself is normally replayable. Existing non-transient HTTP errors, especially the not-found classification used by resource state handling, must keep their current single-attempt `errors.Is` / `errors.As` behavior.

Keep the public client API compatible; this is a transport behavior change, not a new per-resource retry setting.
