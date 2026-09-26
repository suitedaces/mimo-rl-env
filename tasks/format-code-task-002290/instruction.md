## Allow choosing the multiprocessing start method for the `Parallel` executor

When I run a pipeline with the `Parallel` executor (`executor: parallel` in `pipeline.yaml`), Ploomber spawns child processes using whatever the platform default for Python's `multiprocessing` is — on Linux that's `fork`.

The `fork` start method doesn't play well with several libraries I'm using inside my tasks (NumPy/BLAS thread pools, PyTorch with CUDA, gRPC clients, etc.). Symptoms range from child workers hanging forever to occasional crashes that I can't reproduce when I run the same task standalone with `spawn`.

The standard fix for this kind of issue with `multiprocessing` is just to switch the start method to `spawn` (or `forkserver`). But as far as I can tell from the docs at https://docs.ploomber.io/en/latest/api/spec.html#executor, there's no way to tell the `Parallel` executor which start method to use — it's whatever `multiprocessing` picks by default on my system.

It would be great if I could declare this in my `pipeline.yaml`, alongside `processes`, something like:

```yaml
executor:
  dotted_path: ploomber.executors.Parallel
  processes: 2
  # ... some way to ask for spawn/forkserver here
```

so I can switch away from `fork` without having to drop down to the Python API and instantiate the executor myself.

A few things that would be nice:

- support all three values that `multiprocessing` itself supports (`fork`, `spawn`, `forkserver`)
- when nothing is specified, keep behaving exactly like today (use the platform default), so existing pipelines aren't affected
- a clear error if I typo the value, instead of failing later inside the pool

Linking #942.
