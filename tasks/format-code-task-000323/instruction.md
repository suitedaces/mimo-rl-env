aiohttp 3.8.1

`await websocket.receive_json()` Will die with `TypeError` on `WSMsgType.CLOSED`.

#2784 is fixed, yes:

```python
 async def __anext__(self) -> WSMessage:
        msg = await self.receive()
        if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
            raise StopAsyncIteration
        return msg
```

Yes, bug is fixed in iterator but NOT fixed for `websocket.receive_*` functions, like `receive_json()`

I would raise RuntimeError or so if corresponding message "type" (like bytes, str, or json) can not be received.

A dedicated public exception class (something like `WSMessageTypeError`) exported from `aiohttp` would be ideal so users can catch it specifically.
