### Cannot create multiple `JsonApi` clients in the same app

I'm using `devour-api-client` in a project that talks to two different JSON-API backends — our main app API and a separate analytics API. They live on different hosts and need different headers, so I want one Devour client per backend.

The current bootstrap is:

```js
import JsonApi from 'devour-api-client'

let mainApi = JsonApi.getInstance()
mainApi.setup('http://main.example.com')
mainApi.headers['x-auth'] = 'token-for-main'

let analyticsApi = JsonApi.getInstance()
analyticsApi.setup('http://analytics.example.com')
analyticsApi.headers['x-auth'] = 'token-for-analytics'
```

After this runs, `mainApi` and `analyticsApi` are the same object. The second `setup(...)` call overwrites the `apiUrl` and headers of the first one, and any models I defined on `mainApi` show up on `analyticsApi` too. I end up with one shared client instead of two.

Looking at the README, `JsonApi.getInstance()` seems to be the only documented way to obtain a client, and it always hands back the same instance. That makes it impossible to use the library against more than one API at a time, or to have isolated clients in tests.

Could the API be changed so I can create independent `JsonApi` clients? Something where each client has its own `apiUrl`, headers, middleware stack and registered models, and configuring one doesn't leak into another. Happy to update the README example to match.
