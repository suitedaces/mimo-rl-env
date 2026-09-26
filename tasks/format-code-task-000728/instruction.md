## Closing a WAMP session raises errors when a pending call's awaiting task was cancelled (asyncio)

I'm using autobahn-python over asyncio. In my app I make WAMP calls
from inside tasks and put timeouts on them with `asyncio.wait_for`, so
some calls end up with their awaiter cancelled before `session.call(...)`
has actually returned. Roughly:

```python
async def fetch():
    return await session.call(u'com.example.fetch')

try:
    result = await asyncio.wait_for(fetch(), timeout=2.0)
except asyncio.TimeoutError:
    pass  # give up and move on
```

After running like this for a while I eventually shut the session down —
either explicitly via `leave()`, or because the underlying transport
drops. When that happens and there are still-pending requests whose
awaiting task had previously been cancelled / timed out, autobahn itself
errors out during the teardown of the session.

I'd expect closing a session to be a clean operation: even if some of
the still-outstanding request futures have already been abandoned or
cancelled by their callers, shutting the session down shouldn't blow up.
