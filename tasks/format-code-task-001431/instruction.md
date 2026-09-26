## Feature request: gzip-compressed ASC log support

I'm using `can.Logger` / `can.LogReader` to record long CAN sessions to `.asc` files. The plain ASC format is human-readable which is great, but the files get huge — a multi-hour capture easily ends up in the hundreds of MB and they compress down to a fraction of that with gzip, so I end up post-processing every recording with `gzip` afterwards just to archive it.

It would be really nice if python-can supported reading and writing gzipped ASC logs directly, so I could do something like

```python
import can

bus = can.Bus(...)
logger = can.Logger("capture.asc.gz")  # write compressed directly
notifier = can.Notifier(bus, [logger])
```

and later

```python
for msg in can.LogReader("capture.asc.gz"):
    ...
```

without having to manually `gzip`/`gunzip` around the call or wrap a file object myself. The dispatch in `Logger`/`LogReader` already picks the right writer/reader based on the file extension for `.asc`, `.blf`, `.csv` etc., so it'd be natural for compressed ASC files to slot in the same way.

A couple of things that would be useful to support:

- Accept either a path or an already-open file object, matching how the existing ASC reader/writer behave.
- Allow tuning the gzip compression level for the writer (I'd like to trade speed vs. size depending on the machine doing the logging).

The output of the writer should of course still be a valid gzipped ASC file that the matching reader (and standard tools like `zcat`) can decode back into the same messages.

It would also be nice to expose the underlying compressed reader/writer as standalone public classes under `can` (something like `can.GzipASCWriter` / `can.GzipASCReader`, paralleling the existing `can.ASCWriter` / `can.ASCReader`), so they can be instantiated directly when not going through `Logger` / `LogReader`.
