## No way to disable response gzip compression in `HttpServer`

Looking at `HttpServer`, when the servlet context is built it always installs a `GzipHandler` for response compression:

```java
// -- gzip handler
context.insertHandler(new GzipHandler());
```

There's no corresponding switch on `HttpServerConfig` — every service that uses airlift's http-server gets gzipped responses whether it wants them or not.

This is a problem in a few setups we have:

- Services sit behind a reverse proxy / CDN that already handles content negotiation and compression. Doing gzip a second time at the origin is just wasted CPU.
- Some downstream consumers want to look at raw response bodies (debugging, capturing traffic, simple clients that don't speak `Accept-Encoding`) and the automatic gzip layer gets in the way.
- For some endpoints the payloads are already compressed (images, pre-gzipped blobs) and re-running them through `GzipHandler` is pointless.

I'd like to be able to turn the response compression off via configuration, the same way other server features are toggled in `HttpServerConfig` (e.g. the `http-server.log.compression.enabled` flag for request log compression). The default should remain "compression on" so existing deployments don't change behavior — this is purely an opt-out for the cases above.

The new property would be something like `http-server.compression.enabled` on `HttpServerConfig`.
