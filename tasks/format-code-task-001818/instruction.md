## CORS fails when requesting `/{identifier}/info` (without `.json`)

I'm building a IIIF viewer that lives on a different origin from our Loris server. When my front-end JS requests the info endpoint, two URL forms behave differently:

- `GET https://loris.example.org/abcd1234/info.json` — works fine, response has the expected CORS headers, JSON comes back.
- `GET https://loris.example.org/abcd1234/info` (no `.json`) — the browser blocks it with a CORS error and the request never completes.

Looking at the network tab for the failing one, Loris answers with a 303 pointing at `/abcd1234/info.json`, but that intermediate response is missing `Access-Control-Allow-Origin`, so the browser refuses to expose it / follow it from cross-origin JS. The final `info.json` resource itself is fine when I hit it directly — it's only the redirect step that the browser won't accept.

The IIIF Image API spec allows clients to request the info resource via the bare identifier path and expects servers to redirect, so cross-origin clients should be able to use that form too. Right now anyone whose viewer is hosted on a different origin from Loris is forced to always append `.json` themselves, which defeats the point of the redirect.

Could the redirect response from `/{identifier}/info` be made usable by cross-origin clients, the same way the regular `info.json` response already is?
