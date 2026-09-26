## `tff.program` managers are awkward to use from a non-async script

I'm running a fairly standard FL simulation. A simplified version of my main loop looks like this:

```python
import tensorflow_federated as tff

state_manager = tff.program.FileProgramStateManager(root_dir='/tmp/run1')
metrics_manager = tff.program.CSVFileReleaseManager(file_path='/tmp/run1/metrics.csv')

state = training_process.initialize()
for round_num in range(1, total_rounds + 1):
    state, metrics = training_process.next(state, sample_clients(round_num))
    metrics_manager.release(metrics, round_num)
    state_manager.save(state, round_num)
```

The script is a plain top-level Python program — no async framework, no `asyncio.run` wrapper around `main`, just a loop. After upgrading TFF, this stopped working the way it used to. The `release(...)` and `save(...)` calls don't actually do anything on disk anymore — I just get `RuntimeWarning: coroutine '...release' was never awaited` and no files show up. Same story for `FileProgramStateManager.load(...)` / `.versions()` / `.load_latest(...)`, and for the other release managers (`SavedModelFileReleaseManager`, `TensorBoardReleaseManager`, `MemoryReleaseManager`, `LoggingReleaseManager`).

To make my loop work again I now have to wrap every single call:

```python
import asyncio

loop = asyncio.new_event_loop()
for round_num in range(1, total_rounds + 1):
    state, metrics = training_process.next(state, sample_clients(round_num))
    loop.run_until_complete(metrics_manager.release(metrics, round_num))
    loop.run_until_complete(state_manager.save(state, round_num))
```

This is a lot of boilerplate for what conceptually is "write this value to a file", and it's easy to get wrong — reusing the wrong loop, nested-loop errors when something else in the stack also wants an event loop, etc. It also makes the public surface of `tff.program` much harder to teach to people who are just writing a normal simulation script. The same pain shows up inside `tff.simulation.run_training_process`, which similarly has to juggle an event loop just to call into these managers.

For my use case (and I suspect most simulation users) I don't actually need any concurrency from these methods — I want to save state, I want to release metrics, I want to know what versions exist on disk. These are simple, blocking, filesystem-y operations. Could the `ProgramStateManager` / `ReleaseManager` interfaces (and their shipped implementations) expose these operations as ordinary synchronous methods, so calling `manager.save(state, round_num)` or `manager.release(metrics, round_num)` from a regular script just works?
