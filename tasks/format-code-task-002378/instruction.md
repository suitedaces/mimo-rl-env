Error when using settings class that has cli_parse_args=True in VSCode Notebook
### Problem 
Some applications add cli args by default. E.g. VSCode:
<img width="902" alt="image" src="https://github.com/user-attachments/assets/86538f92-19d6-406c-9c62-eb9971bd5f84">

I want to ignore this using:
```python
model_config = SettingsConfigDict(cli_parse_args=True, cli_ignore_unknown_args=True)
```

but if I have a settings class with an attribute that starts with f it will still try to using this argument:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class MySettings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True, cli_ignore_unknown_args=True)

    freeze: bool = False

MySettings()
```

Gives the following error:
```
ValidationError: 1 validation error for MySettings
freeze
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='/home/simon/.local/share...234382f2c59f2a7cbf.json', input_type=str]
    For further information visit https://errors.pydantic.dev/2.9/v/bool_parsing
```
### Root cause

This is because ArgumentParsers allows abbreviations by default:
https://docs.python.org/3/library/argparse.html#allow-abbrev

### Proposed solution
Could you add an option to `SettingsConfigDict` to set `allow_abrev=False` in the `_CliInternalArgParser`?

Maybe this should even be the default, it can be quite confusing if the Settings class by default accepts any abbreviation of an argument as that argument.

### Workarounds
In case anyone is running into the same, the simplest workaround is just not using attributes that start with f. Another solution is to check whether the program is running in ipython and if so set cli_parse_args to false.

### Other error variant
Another fun example:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class MySettings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True, cli_ignore_unknown_args=True)

    freeze: bool = False
    freeze_also: bool = False

MySettings()
```

Output:
```
An exception has occurred, use %tb to see the full traceback.

SystemExit: 2

[/home/simon/miniforge3/envs/asr_test/lib/python3.12/site-packages/IPython/core/interactiveshell.py:3585](https://vscode-remote+ssh-002dremote-002bwsl.vscode-resource.vscode-cdn.net/home/simon/miniforge3/envs/asr_test/lib/python3.12/site-packages/IPython/core/interactiveshell.py:3585): UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
  warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)
usage: ipykernel_launcher.py [-h] [--freeze bool] [--freeze_also bool]
ipykernel_launcher.py: error: ambiguous option: --f=/home/simon/.local/share/jupyter/runtime/kernel-v3f2135e10095ca1cb1e8523234382f2c59f2a7cbf.json could match --freeze, --freeze_also
```
