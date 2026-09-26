Bug: Quality value syntax not supported
It seems like fastify-compress does not support [Quality Value](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Encoding#Syntax) syntax in the `Accepts-Encoding` header. This values for example causes a `406 Unsupported Encoding` HTTP error to be returned. 

Looking int the source of [`index.js:128`](https://github.com/fastify/fastify-compress/blob/master/index.js#L126) in `onSend` the `encoding` variable is indeed `null`. This error goes away once removing the `q` directives from the header value.

Example `Accepts-Encoding` header value that we fail to parse:
`gzip;q=1.0,deflate;q=0.6,identity;q=0.3`

Quickly looking at the source, we will likely need to update`getEncodingHeader` to support this.
