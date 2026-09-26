## `Queue.get()` hangs forever when the queue is empty

I'm trying to write a polling-style consumer with `aio_pika` — periodically pull one message at a time off a queue and process it. The natural code is just:

```python
message = await queue.get()
# ... handle message
```

This works fine when there's actually something on the queue. The problem is when the queue is empty: the `await` blocks indefinitely and never returns. There's nothing in the API right now that lets me detect "the queue is empty at this moment, move on".

I tried using the `timeout` argument as a workaround, which does eventually unblock me, but it's the wrong signal — I get back a generic timeout error that's indistinguishable from "the broker stopped responding" or "the consumer is stuck on something". An empty queue is a perfectly normal, expected outcome of a `get`; conflating it with timeouts/connection failures means I can't write a sensible polling loop on top of it.

Could `Queue.get()` surface "queue is empty" as a first-class result? For example a dedicated exception users can catch, or a way to opt into getting `None` back — anything that distinguishes "empty right now" from "something went wrong while waiting". Right now there's just no good way to use `get()` against a queue that might be empty.

I'd expect the new exception to live under `aio_pika.exceptions` (something like `QueueEmpty`), and the opt-in to be a kwarg on `Queue.get(...)` (something like `fail=False` to switch to the `None`-returning behavior).
