Broken connections with many concurrent `HEAD` requests
Using `waitress==2.1.2` and `pyramid==2.0.2` I've discovered that ~1% of requests fail due to broken connections when there are many concurrent requests.

Requests fail with a `BrokenResourceError` or `ReadError` or `RemoteProtocolError: Server disconnected without sending a response.` or `Connection reset by peer` etc.

The server looks like:

```python
from pyramid.config import Configurator
from pyramid.response import Response

import waitress

import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

def hello_world(request):
    return Response("test")


if __name__ == '__main__':

    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()

    waitress.serve(app, host='127.0.0.1', port=8000, threads=10)
```

If I increase the threads, nothing changes. If I use another WSGI server like `gunicorn`, there are no failed requests.

I'm testing concurrent request success rates with following script:

```python
import httpx
import anyio
import traceback


ATTEMPTS = 1000
TARGET = "http://localhost:8000"
HEAD_FAILURE = []
HEAD_SUCCESS = 0
GET_FAILURE = []
GET_SUCCESS = 0


async def head(client: httpx.AsyncClient, url: str):
    global HEAD_SUCCESS
    try:
        response = await client.head(url)
        response.raise_for_status()
    except Exception as exc:
        HEAD_FAILURE.append(exc)
    else:
        HEAD_SUCCESS += 1

    print(".", end="")


async def get(client: httpx.AsyncClient, url: str):
    global GET_SUCCESS
    try:
        response = await client.get(url)
        response.raise_for_status()
    except Exception as exc:
        GET_FAILURE.append(exc)
    else:
        GET_SUCCESS += 1

    print(".", end="")



async def main():
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=300)) as client:
        async with anyio.create_task_group() as tg:
            for _ in range(ATTEMPTS):
                tg.start_soon(head, client, TARGET)
                tg.start_soon(get, client, TARGET)


anyio.run(main)


# Report

seen = set()
for exc in HEAD_FAILURE:
    if type(exc) in seen:
        continue
    seen.add(type(exc))
    print()
    print()
    traceback.print_exception(exc)
    print()

print()
print(f"Displayed {len(seen)} unique exception types")
print(f"{len(HEAD_FAILURE)}/{len(HEAD_FAILURE) + HEAD_SUCCESS} HEAD requests failed")
print(f"{len(GET_FAILURE)}/{len(GET_FAILURE) + GET_SUCCESS} GET requests failed")
```

I'm testing on macOS with Python 3.11.4.

I discovered this while working with `devpi`, see https://github.com/devpi/devpi/issues/1022.
