## Empty Polkadot own node setting still triggers connection attempts

I'm running rotki to track my Polkadot holdings. A while back I had configured my own Polkadot RPC endpoint in the settings (since I had a local node running), but I've since shut down my own node and want to go back to using the default public nodes.

So I went into the settings, cleared the "own RPC endpoint" field for Polkadot, and saved. From the UI it looks like the setting is gone — the field is empty.

But when I restart rotki (or anytime the Polkadot manager tries to reconnect), I keep getting connection errors related to my own node. It looks like the app is still trying to connect to "my" Polkadot node, except now there's no actual endpoint configured — so it just fails. Looking at the logs I can see it's still attempting a connection on the own-node slot even though there's nothing there to connect to.

Same thing happens for Kusama if I do the equivalent there.

Expected behavior: if I've cleared the own RPC endpoint (i.e. the setting is empty), rotki should treat that as "I don't have my own node" and just skip trying to connect there. It should fall back to the configured public nodes without raising connection errors for an endpoint I never set.

Currently it feels like clearing the field and never having set it should behave the same way, but they don't.
