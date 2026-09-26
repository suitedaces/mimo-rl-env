## Stale `ChannelUpdate` entries pile up in the reliable sender's message store

I run an lnd node and periodically adjust my channel policies (fee changes, timelock tweaks). Some of my peers are flappy — they drop offline for a while and reconnect later. I noticed two things that seem off with the reliable message-sending path that handles "send this gossip message to peer X once they're back online".

### 1. Old `ChannelUpdate`s never get cleaned out

If a peer is offline and I bump my fees a few times, then eventually the peer reconnects and the latest `ChannelUpdate` gets delivered to them — great. But the entry in the persistent message store for that (peer, channel) never goes away. Over weeks of operation I can see these accumulating; the store only grows.

It looks like only `AnnounceSignatures` ever get pruned after delivery. `ChannelUpdate`s seem to be treated as "always fresh" — but in practice, by the time we deliver one (or by the time we look at the store on the next restart), the local graph almost always has a newer version of that policy, and the peer can get the latest one from normal gossip anyway. There's no reason to keep the stale one around forever, and definitely no reason to resend it on restart.

I'd expect: once a queued `ChannelUpdate` is older than what my own graph already knows about that channel/direction, it should be considered stale and dropped from the store, the same way `AnnounceSignatures` are handled today.

### 2. Sends racing against a peer going offline again

I also occasionally see errors in my logs that look like the reliable sender just successfully detected a peer reconnecting and immediately tried to push pending messages to them — and the send fails because the peer is already gone again. This happens with flappier peers. It feels like there's a window between "peer-online notification fires" and "we actually call SendMessage on it" where the peer can disconnect, and we don't recheck before pushing the bytes out. In that case I'd rather have it loop back to waiting for the peer to come online again than burn a failed send and an error log.

### 3. (Minor) No log when a request comes in for an offline peer

While digging into the above, I noticed there's basically zero visibility when a send request arrives for a peer that's currently offline — the request gets buffered to disk silently. A debug log noting "got a message for peer X while they're offline" would have saved me a lot of time figuring out what was happening. Not critical, but it'd be nice.
