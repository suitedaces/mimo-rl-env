## Feature request: produce `tf.train.SequenceExample`s from compiler logs

`compiler_opt/rl/log_reader.py` exposes `read_log`, which yields `Record`s
(features + score per step) from the simple log format the compiler emits.
That's great for inspection, but for actually training a policy we need the
data as `tf.train.SequenceExample`s — that's what the rest of the training
pipeline consumes.

Right now every caller has to hand-roll the conversion: walk the records,
figure out per-spec whether the tensor goes into a float list or an int
list, append step-by-step into feature lists, etc. It's boilerplate that
belongs in `log_reader` itself.

There's also a wrinkle specific to passes like regalloc: a single log file
contains observations spanning multiple "contexts" (for regalloc the context
is a function name, so one module's log covers many functions). These
shouldn't be flattened into a single SequenceExample — observations from
different functions are independent trajectories and need to stay separate.
For passes like the inliner where the context is just `"default"`, there's
effectively one trajectory per log.

Could `log_reader` provide a helper that takes a log file path and returns
the SequenceExamples grouped by context, so callers can just do

```python
examples = log_reader.<the new helper>(path)
# feed examples into training
```

without re-implementing the Record → SequenceExample plumbing in every
training script?

I'd expect the new helper to be named something like `read_log_as_sequence_examples`.
