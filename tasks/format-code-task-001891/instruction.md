Cannot detect kernel during native build on Debian GNU/Hurd
**Describe the bug**
Using `host_machine.kernel()` during a native build on Debian GNU/Hurd causes setup to fail.

The wider context for this is that if `meson env2mfile` is asked to generate a cross-file to build GNU/Hurd binaries based on `dpkg-architecture -ahurd-i386`, it has `kernel='linux'`, which is certainly wrong. To fix that bug (see #13722) I would like it to have its `kernel` set to whatever happens in native builds, but right now, what happens in native builds is an error, which doesn't seem like what anyone wants either.

**To Reproduce**

```
project('test')
message('system is @0@'.format(host_machine.system()))
message('subsystem is @0@'.format(host_machine.subsystem()))
message('kernel is @0@'.format(host_machine.kernel()))
```

outputs:

```
The Meson build system
Version: 1.5.2
Source dir: /home/smcv/meson
Build dir: /home/smcv/meson/_build
Build type: native build
Project name: test
Project version: undefined
Host machine cpu family: x86
Host machine cpu: i686-at386
Message: system is gnu
Message: subsystem is gnu

meson.build:4:43: ERROR: Kernel not defined or could not be autodetected.
```

**Expected behavior**
I expected `host_machine.kernel()` to have some reasonable value, probably either `gnu`, `hurd` or `mach`.

Whatever value is chosen, adding `'gnu': <the chosen value>` to `KERNEL_MAPPINGS` in `mesonbuild/environment.py` would probably be sufficient to resolve this bug.

If I understand correctly, the kernel of a Hurd system is technically the GNU Mach microkernel, but that's an implementation detail that ordinary Unixy software is not expected to interact with? For what it's worth, `uname -s` (`uname --kernel-name`) outputs `GNU` on this system.

**system parameters**
* Is this a cross build? no
* what operating system? Debian unstable
* what Python version? 3.12.6
* what `meson --version`? 1.5.2
* what `ninja --version` if it's a Ninja build? irrelevant, I don't get that far
