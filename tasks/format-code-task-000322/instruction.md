### `FileResponse` doesn't implement Range requests properly

I'm serving large files (video) through `web.FileResponse` and a browser/player that does Range requests is misbehaving against the aiohttp server. Digging into what aiohttp actually returns vs. what other static file servers (nginx, apache) return, several things look wrong:

**1. No `Content-Range` on 206 responses**

When a client sends e.g. `Range: bytes=0-1023`, aiohttp does respond with `206 Partial Content` and the right body slice, but the response is missing the `Content-Range: bytes 0-1023/<file-size>` header. RFC 7233 requires it on 206 responses, and some clients refuse to use the partial response without it (they fall back to redownloading from scratch, or just break).

**2. No `Accept-Ranges` advertised**

Even on a normal 200 response for a static file, aiohttp doesn't tell the client that range requests are supported. Clients that probe with a HEAD first (e.g. download managers, video players doing seek) don't know they can issue Range requests.

**3. Out-of-range start range doesn't return 416**

If the file is 200 bytes and the client sends `Range: bytes=99999-`, aiohttp currently returns the request as if it were satisfiable. Per RFC 7233 the server should return `416 Range Not Satisfiable` here.

**4. Out-of-range tail range breaks the response**

If the file is 200 bytes and the client sends `Range: bytes=-99999` (give me the last 99999 bytes), the request blows up instead of just returning the whole file (which is what nginx etc. do — clamp to start of file).

Minimal repro for #4:

```python
from aiohttp import web

async def handler(request):
    return web.FileResponse('./small_file.txt')   # ~200 bytes

app = web.Application()
app.router.add_get('/', handler)
web.run_app(app)
```

```
$ curl -H 'Range: bytes=-99999' -i http://localhost:8080/
```

…doesn't give back the file the way I'd expect.

---

While we're talking about conditional/range stuff, it would also be nice if `FileResponse` honored `If-Unmodified-Since` and `If-Range` — right now only `If-Modified-Since` is checked, so a client using `If-Range` to revalidate before resuming a download can't actually do conditional ranged GETs against an aiohttp-served file.

Could `FileResponse` be made RFC 7233-compliant for Range requests?
