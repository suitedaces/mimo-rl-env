# Problem Statement

I'm using garage on a torch-only setup and just importing the logger forces tensorflow in because of the tensorboard stuff baked into it. I don't even want tensorboard output here. Could there be some config flag to turn tensorboard off so the logger works without pulling tf? Also it'd be nice if I could re-init the logger between runs instead of carrying state over.

# Expected outcomes

- Tensorboard logging can be controlled through a public configuration flag, `garage.config.LOG_TENSORBOARD`, which defaults to enabled.
- When `garage.config.LOG_TENSORBOARD` is disabled before using the logger, the logger remains usable in a non-TensorFlow setup and tensorboard output is not required.
- The public logger object supports a callable `reset()` operation, and calling it succeeds whether tensorboard logging is enabled or disabled.
- Existing logger functionality such as text/tabular logging, snapshot configuration, and parameter/variant logging continues to work when tensorboard logging is disabled, including use with ordinary output file names that do not include a directory component.
- `garage.misc` exposes the public `logger` object directly, so `from garage.misc import logger` works.

# Implementation notes

- The specific internal organization of the logger, tensorboard integration, and reset mechanism is up to the implementer.
- The tensorboard-disabled mode should avoid requiring TensorFlow-backed tensorboard machinery for ordinary logger use.
- Preserve existing public logger behavior except where tensorboard-specific behavior is intentionally disabled by configuration.
