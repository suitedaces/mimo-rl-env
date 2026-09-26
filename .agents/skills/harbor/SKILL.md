---
name: harbor
description: Build, convert, and validate Harbor tasks, datasets, and RL environments using the official Harbor documentation. Use for work involving Harbor task format, verifiers, Rewardkit, jobs, and datasets.
---

# Harbor

Use the official Harbor docs when designing or implementing tasks and datasets. The [pasted documentation index](references/docs-index-pasted.md) is the user-provided starting point. The [downloaded documentation index](references/docs-index.md) and pages under `references/docs/` are a local snapshot recorded in [snapshot.json](references/snapshot.json). Run `python3 scripts/update_docs.py` from this skill directory to refresh it. Check the live page before relying on details that may have changed.

For task conversions, establish the source task's instruction, execution environment, inputs, expected outputs, and checkable success criteria before writing `task.toml` or verifier code. Keep source-derived facts distinct from proposed design choices. Read only the relevant local docs pages, then validate against the current Harbor CLI and a representative task run when available.

On the locally tested Harbor 0.22.0 CLI, task discovery requires an `environment/` directory even with `[environment].docker_image`, and `harbor run -p` takes the parent dataset directory containing task directories. Check these behaviors against the installed version before reusing them elsewhere.
