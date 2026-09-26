## `responseHeadersEndTime` is unreliable for cached / `data:` requests

I'm doing some custom analysis over Lighthouse's network records — specifically I want the time spent receiving response headers, computed as `responseHeadersEndTime - networkRequestTime` for each request.

For normal requests that actually go to the network this works fine. But for requests that don't do any real network work — memory/disk cache hits, `data:` URLs, etc. — the numbers I get out of `responseHeadersEndTime` don't make sense. Sometimes I get a large negative duration (looks like the field is still at its initial sentinel value), other times the value is just inconsistent with the request's other timings (e.g. it ends up earlier than `networkRequestTime`, or it's some timestamp that doesn't correspond to anything header-related given that nothing was ever fetched from the network).

It seems like the field is just not well-defined for requests where no bytes were ever received over the wire. Right now every downstream consumer that touches `responseHeadersEndTime` has to know "oh, but if it's a cached request / data URL then this is garbage, special-case it" — which is easy to get wrong and not really documented anywhere.

It'd be much nicer if `NetworkRequest` itself guaranteed a coherent value for `responseHeadersEndTime` in these cases — pick whatever fallback makes semantic sense (there was no network activity, so any timing for "when headers finished arriving from the network" is a bit fictional anyway), and document what that fallback means on the field itself so consumers don't have to reverse-engineer it. The important thing is that the field is always in a sensible relationship to the request's other timing fields, regardless of whether the request actually hit the network.
