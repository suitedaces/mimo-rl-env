### Temporary containers run with `--tty` but without `--interactive`

When I use `Image.run()` to start a temporary container (the default `temporary=True`), the generated `docker run` command includes `--tty` but not `--interactive`. In practice `-t` is almost always paired with `-i` — without `-i` you can't actually type into the container, signals like Ctrl-C don't get forwarded properly, etc.

Reproduction is just calling run on any image:

```python
from fabricio.docker import Image
img = Image('alpine')
img.run('sh')
```

The resulting `docker run` line carries `--tty` but no `--interactive`, so the shell isn't really usable interactively.

I'd expect a temporary container to be both tty-allocated and interactive (and conversely, when it's not temporary, neither flag should be set), matching the typical `docker run -it` usage pattern.
