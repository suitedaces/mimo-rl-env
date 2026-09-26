## Graceful shutdown: new request streams during the grace period aren't rejected cleanly

I'm using `http3.Server` and testing rolling restart behavior. The flow is:

1. server is up, a client has an open HTTP/3 connection (kept around for reuse)
2. I call `server.Shutdown(ctx)` with some reasonable grace timeout
3. around the same time the client opens a new request stream on the existing connection (in practice this happens because GOAWAY is in flight, or the client just hasn't processed it yet)

What I'd expect: the GOAWAY tells the client "anything above stream ID X is not going to be handled, you should retry it elsewhere." Per HTTP/3 the server should then refuse those late streams in a way the client can recognize as "this request was rejected, safe to retry on a new connection."

What I actually see: those late request streams just sit there. They don't get handed to my handler (which is correct), but they also don't get rejected in any way the client can act on. Nothing comes back until eventually my `Shutdown` context expires and the whole connection gets torn down — at which point the client treats those requests like any other connection failure, with no signal that they were specifically rejected because of an in-progress drain.

For a graceful drain to actually be useful for clients (so they can confidently retry the rejected requests against another instance) the server needs to keep responding to those late streams during the grace period and explicitly reject them, not silently ignore them until the connection goes away.

In-flight requests that were already accepted before `Shutdown` was called should keep running to completion (or until the grace ctx fires) — that part works fine today, it's specifically the streams that arrive *after* GOAWAY that aren't handled correctly.
