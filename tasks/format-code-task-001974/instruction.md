## Pool has no shutdown story — items it created leak when the app stops

I'm following the channel pooling pattern from the docs (`docs/source/examples/pooling.py`): one `Pool` produces AMQP connections, a second `Pool` produces channels on top of that. The pools work fine while the app is running — items get created lazily, reused, returned. The problem hits when I try to tear everything down cleanly.

Roughly what my code looks like:

```python
connection_pool = Pool(get_connection, max_size=2, loop=loop)
channel_pool    = Pool(get_channel, max_size=10, loop=loop)

task = loop.create_task(consume())
await asyncio.wait([publish() for _ in range(10000)])
await task
# ... now what?
```

At this point I want to release everything the pools created — but there's nothing on the `Pool` API for that. The pool is internally hanging on to all the connections and channels it ever constructed, and I have no handle to ask it to drop them. When the loop exits I get the usual warnings about resources still alive, and the second pool has the same problem layered on top.

I also can't write `async with connection_pool, channel_pool:` around my code, which would be the natural asyncio idiom for "scope these to this block and tear them down on exit." Right now I'd have to keep my own parallel list of every connection / channel that ever passed through the pool just to close them by hand, which kind of defeats the point of letting the pool manage them.

Could `Pool` take responsibility for cleaning up the items it created? Ideally:

- some way to tell a pool "we're done, drop everything you made,"
- support for using it as an `async with` block so cleanup happens on exit,
- once a pool has been shut down, further use of it should fail loudly rather than silently doing whatever it does today.

I'd expect the explicit shutdown to be something like `await pool.close()`, and a way to inspect state via a property like `pool.is_closed`.
