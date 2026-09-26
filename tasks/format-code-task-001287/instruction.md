## Need a way to return a raw (non-serialized) response from a REST endpoint without using streaming

Currently any value returned from a REST handler goes through `_createResponse`, which serializes it as JSON (or HTML if the client asks for it via Accept). That's fine for the normal case, but it means there's no way to return a response that should be sent through verbatim — for example, a handler that produces a plain text blob, an already-encoded payload, or some custom mime-typed content.

For instance, if I write a handler like:

```python
@access.public
def getRawThing(self, params):
    cherrypy.response.headers['Content-Type'] = 'text/plain'
    return 'hello\nworld\n'
```

what actually goes over the wire is `"hello\nworld\n"` (quoted, escaped, `Content-Type: application/json`) because `_createResponse` JSON-encodes whatever I return and overwrites the content type.

The only escape hatch today is to make the endpoint a streaming response. That works, but it's overkill when the payload is small and already fully in memory — I have to restructure the handler to yield/iterate just to avoid the serialization step, and it makes simple endpoints (e.g. returning a short text snippet, an SVG string, a pre-rendered HTML fragment) feel awkward.

It would be nice to have a first-class, non-streaming way for a handler to declare "don't serialize my return value, send it as-is" so the standard request/response flow still applies (CORS, error handling, etc.) but the body is passed through untouched. Ideally it should be usable both from inside the handler body and as a decorator on the route function, and reachable from `Resource` subclasses the same way other helpers like `getBodyJson` are.
