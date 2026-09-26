pip 20.0.2 does not support relative paths for cache dir
In [this PR](https://github.com/pypa/pip/pull/7542) `pip` starts relying on path normalization outside of `WheelCache` class, while it is still being [instantiated manually](https://github.com/jazzband/pip-tools/blob/master/piptools/repositories/pypi.py#L287) by `pip-tools` without path normalization.

Using normalized path should be backward compatible with older versions of pip as well, so it should be safe to do path normalization on `pip-tools` side.

### Steps to reproduce:
```bash
> python3 -m venv venv
> venv/bin/pip install -U pip pip-tools
Collecting pip
  Downloading https://files.pythonhosted.org/packages/54/0c/d01aa759fdc501a58f431eb594a17495f15b88da142ce14b5845662c13f3/pip-20.0.2-py2.py3-none-any.whl (1.4MB)
     |████████████████████████████████| 1.4MB 3.8MB/s 
Collecting pip-tools
  Downloading https://files.pythonhosted.org/packages/db/e3/e9c864e62c5e61f1fa6c3b6232cef135ce7365ceb4b1cfa145e47753ab07/pip_tools-4.4.1-py2.py3-none-any.whl (41kB)
     |████████████████████████████████| 51kB 47.7MB/s 
Collecting six (from pip-tools)
  Downloading https://files.pythonhosted.org/packages/65/eb/1f97cb97bfc2390a276969c6fae16075da282f5058082d4cb10c6c5c1dba/six-1.14.0-py2.py3-none-any.whl
Collecting click>=7 (from pip-tools)
  Downloading https://files.pythonhosted.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl (81kB)
     |████████████████████████████████| 81kB 52.6MB/s 
Installing collected packages: pip, six, click, pip-tools
  Found existing installation: pip 19.2.3
    Uninstalling pip-19.2.3:
      Successfully uninstalled pip-19.2.3
Successfully installed click-7.0 pip-20.0.2 pip-tools-4.4.1 six-1.14.0
> env XDG_CACHE_HOME='.cache' venv/bin/pip-compile --build-isolation reqs.in --output-file reqs.txt
Traceback (most recent call last):
  File "venv/bin/pip-compile", line 10, in <module>
    sys.exit(cli())
  File "venv/lib/python3.8/site-packages/click/core.py", line 764, in __call__
    return self.main(*args, **kwargs)
  File "venv/lib/python3.8/site-packages/click/core.py", line 717, in main
    rv = self.invoke(ctx)
  File "venv/lib/python3.8/site-packages/click/core.py", line 956, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "venv/lib/python3.8/site-packages/click/core.py", line 555, in invoke
    return callback(*args, **kwargs)
  File "venv/lib/python3.8/site-packages/click/decorators.py", line 17, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "venv/lib/python3.8/site-packages/piptools/scripts/compile.py", line 275, in cli
    repository = PyPIRepository(
  File "venv/lib/python3.8/site-packages/piptools/repositories/pypi.py", line 66, in __init__
    self.session = self.command._build_session(self.options)
  File "venv/lib/python3.8/site-packages/pip/_internal/cli/req_command.py", line 83, in _build_session
    assert not options.cache_dir or os.path.isabs(options.cache_dir)
AssertionError
```
