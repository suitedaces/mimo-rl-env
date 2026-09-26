## Hooks directory monitor gets out of sync with the filesystem

I'm using podman's hook directory monitoring (dropping `*.json` files into a hooks.d directory and letting podman pick them up at runtime). I've run into a few situations where what podman thinks is in the directory doesn't match what's actually there.

### 1. One bad hook file hides the other valid hooks

If I drop two hook files into the directory and one of them is malformed (bad JSON / fails validation), the valid one next to it doesn't get picked up either. I'd expect podman to log/report the error for the bad file but still register the good one — instead the good hook is silently missing.

This shows up both at startup and while the monitor is running: as soon as something invalid is in the directory, working hooks alongside it stop being honored.

### 2. `mv`-ing a hook file out of the directory leaves it active

If I `mv somehook.json /tmp/` (instead of `rm`-ing it), podman keeps acting like `somehook.json` is still installed and keeps running it on container start. The file is no longer in the hooks directory, so it shouldn't be applied anymore.

`rm` works correctly; `mv` out of the directory does not.

### 3. Renaming a hook file makes it run twice

If I rename a hook file in place — e.g. `mv myhook.json myhook-renamed.json` within the hooks directory — podman ends up running the hook twice on the next container: once under the old name (which it never dropped) and once under the new name. Only the renamed file actually exists on disk, so it should run once.

### 4. `chmod` on a hook file isn't reflected

Changing permissions on a hook file (e.g. so it becomes unreadable, or fixing it back) doesn't seem to cause the monitor to re-evaluate the directory — the in-memory state just stays whatever it was.

---

In all of these cases, what I'd like is simple: the set of active hooks should match the set of valid `*.json` files currently in the configured hook directories. Errors on individual files should be reported but shouldn't prevent the rest from loading, and filesystem operations like rename/move/chmod should be reflected the same way create/delete already (mostly) are.
