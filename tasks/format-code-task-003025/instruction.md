## `err.timeout` is missing when the request actually times out via xhr

I'm using fetchr's HTTP client with a configured `timeout` and handling failures in my callback. I rely on `err.timeout` to log/report the timeout value that was in effect for the failed request.

It works inconsistently:

- When the server responds with HTTP 408, my failure handler receives an `err` object with `err.timeout` set to the configured timeout. 👍
- But when the request actually times out on the client side (the xhr layer fires its own timeout error before any response comes back), the `err` I get has no `timeout` property at all — it's `undefined`.

Repro is basically:

```js
http.get(url, headers, { timeout: 1000 }, function (err, resp) {
    if (err) {
        console.log('timeout was:', err.timeout); // undefined when xhr times out
    }
});
```

Point a slow endpoint at it (or anything that doesn't respond within 1s) and you'll see `err.timeout` is undefined, even though the failure was clearly caused by the configured timeout.

I'd expect `err.timeout` to be populated whenever the failure is timeout-related, regardless of whether it came back as a 408 status or as an xhr-level timeout error. Otherwise consumers can't reliably tell from the error object what timeout value was in play.
