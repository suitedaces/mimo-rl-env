## `dcos-launch` library API is awkward to use — every launcher method demands the config/info dict be passed in again

I'm trying to use `dcos-launch` as a library (not just through the CLI) to spin up a cluster, wait for it, run some checks, and tear it down. The current launcher API feels really clunky:

```python
import launch, launch.config

config = launch.config.get_validated_config(config_path)
launcher = launch.get_launcher(config)
info = launcher.create(config)
launcher.wait(info)
launcher.describe(info)
launcher.test(info, 'py.test')
launcher.delete(info)
```

A couple of things bother me here:

1. I already handed `config` to `get_launcher(...)` so it could build the right `BotoWrapper` / `AzureWrapper`. Then I have to hand the same `config` to `create(...)` again. Why does the launcher need it twice?

2. After `create`, every subsequent call (`wait`, `describe`, `test`, `delete`) needs me to thread the `info` dict back in as the first argument. The launcher object itself knows which deployment it's responsible for — at least it should — so making me carry `info` around on every call feels redundant. If I forget and call `launcher.wait()` I get a `TypeError`; if I accidentally pass a stale dict I get really confusing behavior.

The natural way to use a launcher feels like:

```python
launcher = launch.get_launcher(config_or_info)
launcher.create()
launcher.wait()
launcher.describe()
launcher.test('py.test')
launcher.delete()
```

i.e. the launcher should own the configuration / deployment state it needs, and each method just acts on that state. `create()` still returns the info dict so I can persist it to disk for a later process to pick back up via `get_launcher(info)`.

Could the AWS and Azure launchers (and the CLI that drives them) be refactored so callers don't have to keep feeding the same dict back in on every method call?
