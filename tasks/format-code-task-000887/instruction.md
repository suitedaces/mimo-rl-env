Telegram clients cannot be checked against an ACL
Telegram IDs are integer numbers, which means they fail to be used by `fnmatch` directly.

``` python
  File "/Users/pavel/.virtualenvs/mybot/lib/python3.5/site-packages/errbot/core.py", line 344, in _process_command_filters
    msg, cmd, args = cmd_filter(msg, cmd, args, dry_run)
  File "/Users/pavel/.virtualenvs/mybot/lib/python3.5/site-packages/errbot/core_plugins/acls.py", line 76, in acls
    if 'allowusers' in acl and not glob(usr, acl['allowusers']):
  File "/Users/pavel/.virtualenvs/mybot/lib/python3.5/site-packages/errbot/core_plugins/acls.py", line 22, in glob
    return any(fnmatch.fnmatchcase(text, pattern) for pattern in patterns)
  File "/Users/pavel/.virtualenvs/mybot/lib/python3.5/site-packages/errbot/core_plugins/acls.py", line 22, in <genexpr>
    return any(fnmatch.fnmatchcase(text, pattern) for pattern in patterns)
  File "/Users/pavel/.pyenv/versions/3.5.1/lib/python3.5/fnmatch.py", line 71, in fnmatchcase
    return match(name) is not None
TypeError: expected string or bytes-like object
```
