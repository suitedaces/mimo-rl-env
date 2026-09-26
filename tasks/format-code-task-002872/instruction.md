tox.ini parsing regression with globbed modules
Our CI suddenly stopped working with `tox==4.0.13`.  `4.0.12` works as expected.  The command is `tox -l`

config file has globbed submodules which look like this: ` [mypy-rest_framework.compat.*]`. Tox seems to choke here.

https://github.com/tfranzel/drf-spectacular/blob/7bfcfb16fe63556f0c6044a4fda4d41cca058051/tox.ini#L97

```
File "/opt/hostedtoolcache/Python/3.10.9/x64/bin/tox", line 8, in <module>
    sys.exit(run())
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/run.py", line 19, in run
    result = main(sys.argv[1:] if args is None else args)
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/run.py", line 45, in main
    result = handler(state)
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/session/cmd/legacy.py", line 105, in legacy
    return list_env(state)
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/session/cmd/list_env.py", line 27, in list_env
    active = dict.fromkeys(state.envs.iter())
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/session/env_select.py", line 333, in iter
    for name, env_info in self._defined_envs.items():
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/session/env_select.py", line 176, in _defined_envs
    env_name_to_active = self._env_name_to_active()
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/session/env_select.py", line [15](https://github.com/tfranzel/drf-spectacular/actions/runs/3721512771/jobs/6316917714#step:5:16)1, in _env_name_to_active
    for name in a_collection:
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/config/source/ini.py", line 70, in envs
    for name in self._discover_tox_envs(core_config):
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/config/source/ini.py", line 86, in _discover_tox_envs
    register_factors(section.names)
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/config/source/ini_section.py", line [18](https://github.com/tfranzel/drf-spectacular/actions/runs/3721512771/jobs/6316917714#step:5:19), in names
    elements = list(extend_factors(self.name))
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/config/loader/ini/factor.py", line 41, in extend_factors
    for group in find_factor_groups(value):
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/config/loader/ini/factor.py", line 65, in find_factor_groups
    for env in expand_env_with_negation(value):
  File "/opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/tox/config/loader/ini/factor.py", line 80, in expand_env_with_negation
    raise ValueError(variant_str)
ValueError: mypy-rest_framework.compat.*
```
