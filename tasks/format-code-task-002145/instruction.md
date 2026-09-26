# Add a `transformRequest` option (and `mapbox://` style URL support)

The top-level entry points that turn a Mapbox Style into an OpenLayers map —
`olms()` and `apply()` — currently give callers no way to influence how the
library fetches the resources it needs (the style document and sprite data).
People behind proxies, or who need to add auth headers / credentials, or who
want to rewrite URLs, have no hook.

Add an optional `options` object as the **last** argument of both `olms()` and
`apply()`. When omitted it must default to no-op behavior, i.e. everything keeps
working exactly as it does today. The object supports the following properties.

## `transformRequest`

A callback `function(url, resourceType)` that is invoked immediately before the
library fetches a resource, giving the caller a chance to alter the request.

- It is called with two arguments: the resolved resource `url` (a string) and a
  `resourceType` string identifying what is being fetched.
- The `resourceType` is `'Style'` for the Mapbox Style document (only fetched
  when the style is passed as a URL, not as an object), and `'Sprite'` for the
  sprite index JSON document.
- If the callback returns a `Request` object, that `Request` is what gets
  fetched instead of the original URL.
- If the callback returns nothing (a falsy value), the original `url` is fetched
  unchanged.

The callback must actually drive the network request: when it redirects a fetch
to a different resource, that other resource is the one that ends up being
loaded.

## `accessToken` and `mapbox://` style URLs

Allow the `style` argument to be a `mapbox://styles/<user>/<id>` URL. Such a URL
must be resolved to its public HTTPS form before being fetched:

```
mapbox://styles/<user>/<id>
  ->  https://api.mapbox.com/styles/v1/<user>/<id>?access_token=<accessToken>
```

where `<accessToken>` is the value of `options.accessToken`. The resolved HTTPS
URL is the one that is fetched, and it is also the `url` passed to
`transformRequest(url, 'Style')`.

Plain `http(s)://` style URLs and style objects must continue to behave as
before.
