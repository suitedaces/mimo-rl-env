## `response.data` comes back as a plain dict instead of the typed object

I'm writing unit tests against code that calls the Steamship SDK. After a call returns I'd like to assert on individual fields the natural way — using attribute access on the returned object, e.g.

```python
response = some_steamship_call(...)
assert response.data.file.blocks[0].tags == [...]
```

But this blows up because `response.data` is actually a plain `dict` at that point, not the typed model I was expecting. To get at the fields I have to fall back to string-keyed dict access:

```python
assert response.data["file"]["blocks"][0]["tags"] == [...]
```

This is painful for a few reasons:

- No IDE autocomplete on the nested fields — easy to typo a key and not catch it until runtime.
- No static type checking; the dict is `Dict[str, Any]` so everything underneath is opaque.
- Tests end up coupled to the exact JSON-y key spelling instead of the model field names.

It looks like the body of the response is being serialized into a dict somewhere on the way back, even when I had (or could have had) the real typed model in hand. I'd like `response.data` to keep the original typed object so attribute access works in tests and downstream code. The dict form is only useful right before going over the wire — by the time it lands in `response.data` on the client side it should be the structured object again.
