## Non-HTTP socket traffic blows up when HTTPretty is enabled

I'm using HTTPretty to mock HTTP responses in my tests, but the code under
test also opens a regular TCP connection to a non-HTTP service (in my case
Redis, but it would happen with anything that's not on ports 80/443). As
soon as that code path calls `send()` or `recv()` on its socket, the test
explodes with:

```
RuntimeError:
HTTPretty intercepted and unexpected socket method call.
Please open an issue at 'https://github.com/gabrielfalcao/HTTPretty/issues'
And paste the following traceback:
...
```

Roughly what I'm doing:

```python
@httprettified
def test_something():
    httpretty.register_uri(httpretty.GET, "http://example.com/api", body="ok")

    # this part of the code talks HTTP — fine, gets mocked
    do_http_call()

    # this part talks to e.g. redis on a non-HTTP port — boom
    do_non_http_call()
```

The HTTP mocking itself works as expected. The problem is that *every*
socket created while HTTPretty is enabled has its `send` / `sendto` /
`recv` / `recvfrom` / `recv_into` / `recvfrom_into` replaced with a stub
that always raises, regardless of whether the socket is actually talking
to something HTTPretty cares about.

I'd expect HTTPretty to only intercept sockets that are actually being
used for HTTP traffic, and to leave other sockets alone so they behave
like normal sockets. Otherwise it's pretty much impossible to use
HTTPretty in any test where the code under test also touches a non-HTTP
service.
