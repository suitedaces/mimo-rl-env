# Add a file-watching utility

We want marimo to be able to react when a notebook file changes on disk (for
example, to reload an app when the underlying `.py` file is edited by another
tool). As a first building block we need a small, reusable file-watching
utility in marimo's internal utils package.

## What to build

Add a `FileWatcher` to `marimo._utils.file_watcher` with the following public
contract.

### Construction

`FileWatcher.create(path, callback)` returns a `FileWatcher` instance that
watches a single file at `path` (a `pathlib.Path`).

`callback` is an **async** function that takes a single `pathlib.Path`
argument. The watcher invokes it whenever it observes that the watched file has
changed.

The watcher must work whether or not the optional `watchdog` package is
installed: if `watchdog` is available it may be used, otherwise the watcher
falls back to polling the file's modification time (roughly once per second).
Either way the observable behavior below must hold.

### Lifecycle

- `start()` begins watching. It must be safe to call from within a running
  asyncio event loop; the callback is scheduled on that loop.
- `stop()` stops watching. After `stop()` is called, no further callbacks are
  delivered, even if the file changes again afterward.

### Behavior

- When the watched file is modified (its contents/modification time change
  after watching begins), the watcher invokes `callback` with the path it is
  watching. The path passed to the callback must equal the `path` that was
  given to `create`.
- While the file is not modified, the callback is not invoked.
- Each subsequent modification triggers another callback, so several edits over
  the lifetime of the watcher result in several callback invocations.

The watcher is for a single file; you do not need to support directories.
