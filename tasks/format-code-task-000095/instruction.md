origin in options with regexp value is broken
According to https://googlechrome.github.io/sw-toolbox/docs/master/tutorial-api.html:

> The origin option is specific to the router methods, and can be either an exact string or a Regexp against which the origin of the Request must match for the route to be used.

So if I had 

```
runtimeCaching: [{
  urlPattern: /^https:\/\/example\.com\/api/,
  handler: 'networkFirst'
}, {
  urlPattern: /\/articles\//,
  handler: 'fastest',
  options: { origin: /twitter\.com/}
}]

```

We would actually get `origin: {}`.

As in https://github.com/GoogleChrome/sw-precache/blob/master/lib/sw-precache.js#L213, `JSON.stringify({origin: /twiter\.com/})` would give us `"{"origin":{}}"`
