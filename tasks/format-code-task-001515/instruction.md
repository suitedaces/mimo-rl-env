RPC client doesn't handle optional path parameters
### What version of Hono are you using?

4.5.6

### What runtime/platform is your app running on?

Cloudflare Pages / Workers

### What steps can reproduce the bug?

1. Make an endpoint with an optional path param, e.g. `/something/:firstId/:secondId/:version?`
2. Try to call the endpoint without the optional parameter using the Hono RPC client, e.g. `client.something[":firstId"][":secondId"][":version?"].$get`

### What is the expected behavior?

We would expect it to call e.g. `GET /something/first/second`.

### What do you see instead?

It instead calls either `GET /something/first/second/:version`, `GET /something/first/second/undefined`, or `GET /something/first/second/null`, depending on how you try to avoid the optional parameter.

### Additional information

Based on my analysis of https://github.com/honojs/hono/blob/main/src/client/client.ts I believe this functionality was simply forgotten / not handled (I do not see any handling of undefined `pathParam`s currently).  Seems like an oversight?  But we would definitely like to utilize this since Hono supports it on the router / server side.

Thank you in advance!
