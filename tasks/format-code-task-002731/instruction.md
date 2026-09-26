## Isolate crashes when error handling path itself fails

I'm running an aqueduct-based HTTP server and occasionally seeing the whole isolate die, taking out subsequent requests on it. After narrowing it down, the crashes seem to happen on the framework's error-handling path itself — not on the original handler's exception. I've reproduced two distinct patterns:

### 1. Responding to a request that has already been responded to

If something in my handler responds to the request and then throws afterwards (cleanup that goes wrong, a follow-up operation that fails, an exception from inside an async continuation, etc.), the framework's catch block tries to send a `500` response on top of the one that already went out. Instead of just losing that one request, the resulting exception isn't caught anywhere and the whole isolate goes down.

Small repro of the shape:

```dart
class MyHandler extends RequestHandler {
  @override
  Future<RequestHandlerResult> processRequest(Request req) async {
    req.respond(new Response.ok({"hello": "world"}));
    throw "post-respond failure";   // simulate cleanup blowing up
  }
}
```

The first response is fine, but the throw triggers the framework's error path, which tries to `respond` again, and the isolate dies.

### 2. Logging after the response is closed

Even when the framework doesn't try to double-respond, the logging done by the error handler ends up calling something like `req.toDebugString(...)`, which reaches into the request's connection info / remote address. In some circumstances (looks like once the underlying response has been closed), that info isn't available anymore and the debug-string construction itself blows up — again on the catch path, again uncaught, again taking the isolate with it.

### What I'd expect

A single misbehaving request shouldn't kill the isolate and stop the server from handling anything else. Even when the error-handling path itself can't do its job (response already sent, connection info gone, etc.), it should fail quietly for that one request and let the server keep serving.
