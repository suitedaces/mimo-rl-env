## `ValueError` from hyperframe leaks out of `receive_data`

I'm writing an HTTP/2 server with `h2`. My main loop looks roughly like this:

```python
conn = H2Connection(client_side=False)
# ... initiate, send preamble, etc.

while True:
    data = sock.recv(65535)
    if not data:
        break
    try:
        events = conn.receive_data(data)
    except ProtocolError:
        # graceful shutdown: send whatever h2 wants us to send,
        # close the socket, log the peer.
        ...
    else:
        handle(events)
```

This works fine for well-behaved peers. But while testing against a peer that sends garbage / malformed bytes (in my case it was a buggy client, but you can also hit this with random fuzzing input on the socket), my server didn't go through the `except ProtocolError` branch — it crashed with a `ValueError` instead, and the whole connection-handling task died.

As far as I can tell from the public API I'm allowed to use, the contract is "feed bytes in, catch `ProtocolError` (and friends defined in `h2.exceptions`) on the way out." A bare `ValueError` bubbling up from inside `receive_data` doesn't fit that contract — I have no reasonable way to know in advance that I also need to catch `ValueError` here, and even if I did, I can't tell it apart from a `ValueError` that genuinely came from a bug in *my own* code further down the stack.

The bytes I was feeding in were definitely bogus at the framing layer (so the peer is at fault, not me). I'm fine with the connection being torn down — that's the right thing to do. I just expect `h2` to surface this as one of its own protocol-level exceptions so my existing error handling can deal with it uniformly, instead of letting an exception type from a lower-level dependency escape through `receive_data`.

Could `h2` make sure that invalid framing input coming in through `receive_data` is reported as a `ProtocolError` (and the connection is torn down accordingly), rather than letting `ValueError` leak out?
