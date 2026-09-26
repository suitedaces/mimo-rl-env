## HttpEndpoint should use Akka HTTP's `Uri` type instead of `java.net.URI`

The rest of our stack is built on Akka HTTP, where URIs are represented by
`akka.http.scaladsl.model.Uri` (or `akka.http.javadsl.model.Uri` on the
Java side). However, `squbs-httpclient`'s `HttpEndpoint` exposes its URI
field as `java.net.URI`, which forces users to bounce between two URI
representations.

For example, on the Java side I already have an
`akka.http.javadsl.model.Uri` in hand (built via the Akka HTTP Uri APIs we
use throughout the rest of the codebase) and I'd like to construct an
`HttpEndpoint` from it:

```java
akka.http.javadsl.model.Uri uri = /* obtained from elsewhere in the
                                     Akka HTTP code we already use */;
HttpEndpoint ep = HttpEndpoint.create(uri, Optional.empty(), Optional.empty());
```

But there's no `create` overload that takes an Akka `Uri` — only ones
taking a `String` (which then internally constructs a `java.net.URI`). I
have to call `uri.toString()` and let `HttpEndpoint` parse it back, which
feels backwards given we're already in Akka-HTTP land.

The same mismatch shows up on the Scala side: `HttpEndpoint.uri` has type
`java.net.URI`, even though everything downstream (the connection pool,
TLS, etc.) is Akka HTTP. It would be much more natural for `HttpEndpoint`
to model its URI with the Akka HTTP `Uri` type so that the whole
`squbs-httpclient` API speaks the same vocabulary as the library it wraps.

Could `HttpEndpoint` be changed to use Akka HTTP's `Uri` type, including a
Java-friendly constructor that accepts `akka.http.javadsl.model.Uri`
directly?
