## `pystack core` fails on core dumps from Python scripts launched via shebang

I have a Python script that I run directly with a shebang (i.e. it starts
with `#!/usr/bin/env python3`, it's `chmod +x`'d, and I just execute it as
`./myscript.py`). The script crashed and produced a core dump, and I wanted
to use pystack to inspect what the interpreter was doing at the time.

When I run

```
pystack core ./core.12345
```

without specifying an executable (the second positional argument is
documented as optional), pystack picks up an executable automatically and
then bails out complaining that what it picked up isn't a valid executable
— it looks like it grabbed the path to my `.py` script itself, not the
`python3` binary that was actually running it. That makes some sense
because for shebang-launched scripts the kernel does record the script
path as the "executable" of the process, but it's not what pystack
actually needs to analyze the core.

As a workaround I can pass the interpreter explicitly:

```
pystack core ./core.12345 /usr/bin/python3
```

and then everything works fine. But this is annoying — the core file
clearly contains enough information about the real interpreter that was
loaded (I can pass it by hand and it just works), so pystack shouldn't
have to give up and demand that I supply it manually for what's a pretty
common way of running Python scripts.

It would be great if `pystack core`, when run without an explicit
executable, could recover in this situation instead of immediately erroring
out, so that the shebang-script case works out of the box.
