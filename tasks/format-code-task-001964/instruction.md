## Connecting with only `authSource` in the URI (no username/password) throws "No auth provider for DEFAULT defined"

I'm trying to connect to a MongoDB instance that doesn't require authentication, but my connection string includes `authSource` (it comes from a shared config template we use across environments — some envs have credentials, some don't).

Minimal repro:

```js
const { MongoClient } = require('mongodb');

const client = new MongoClient('mongodb://localhost:27017/?authSource=admin');
await client.connect();
```

This throws an error along the lines of `No auth provider for DEFAULT defined` when the driver tries to set up the connection.

If I drop `authSource` from the URI entirely, the connection works fine. So the driver clearly doesn't *need* to authenticate here — it just chokes because `authSource` is present without any accompanying username/password.

My read of the MongoDB connection string spec is that `authSource` on its own (without any other credential-related options) should be a no-op — there's nothing to authenticate with, so there's no auth source to apply. The driver shouldn't be forcing an auth handshake in this case.

Could the driver treat a URI that specifies *only* `authSource` (and no username, password, or auth mechanism properties) as effectively unauthenticated, so the connection just goes through?
