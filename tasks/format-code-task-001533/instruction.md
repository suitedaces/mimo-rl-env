## Support cancelling an in-flight `client.post()` call

I'm using `crosspost` from a CLI/service that fans a single message out to several networks at once (Bluesky, Mastodon, Twitter, Discord, LinkedIn). It works great in the happy path, but I can't find any way to **cancel** a post once `client.post()` is running.

Two cases where this hurts:

1. **Timeouts.** One of the upstream services (any of them — pick your favourite) occasionally takes 30+ seconds to respond. I'd like to give the whole call a budget and bail out if it doesn't finish in time.
2. **User-initiated cancel.** The app has a "Post" button and a "Cancel" button next to it. If the user hits Cancel while the requests are still in flight, I want to actually stop the requests, not just ignore the eventual result.

Right now `client.post(message, postOptions)` returns a promise I can't interrupt. I can wrap it in `Promise.race` against a timeout, but that only lets *my* code move on — the underlying HTTP requests keep running in the background until each strategy's `fetch` finishes, which wastes API quota and connections.

The rest of the Node / Web ecosystem (`fetch`, `undici`, most HTTP clients) accepts an `AbortSignal` for exactly this. It would be great if `client.post()` accepted one too via `postOptions`, and propagated it down so that aborting the controller actually rejects the in-flight network calls across all the strategies — not just `Client`, but each individual strategy when used directly (`BlueskyStrategy`, `MastodonStrategy`, `TwitterStrategy`, etc.), since I sometimes use a single strategy on its own.

Rough shape of what I'd like to be able to write:

```js
const controller = new AbortController();

// somewhere else: controller.abort() when the user clicks Cancel
//   or: setTimeout(() => controller.abort(), 30_000) for a timeout

await client.post("Hello world!", {
    images: [...],
    // a way to pass controller.signal here
});
```

After abort, I'd expect the promise from `post()` to reject (per strategy where applicable, since `Client` already aggregates with `Promise.allSettled`) rather than resolve with whatever the server eventually returned.
