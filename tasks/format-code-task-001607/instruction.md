`cloup.Group` ignores `command_class` to produce sub-commands
Using:
- Cloup v2.1.1
- Click v8.1.4
- Python 3.11.4

#### Bug description

`cloup.Group` ignore the [`command_class` property](https://github.com/pallets/click/blob/d9af5cfa009c927a96d10ed38a3e37979876a12e/src/click/core.py#L1797-L1802) that is [used in `click.Group` to set the default class of the `@group.command()` decorator](https://github.com/pallets/click/blob/d9af5cfa009c927a96d10ed38a3e37979876a12e/src/click/core.py#L1855-L1894).

#### To Reproduce

Here is the minimal CLI, saved in a `cloup_test.py` file, that is reproducing the issue:

```python
from cloup import Command, Group, group


class CustomCommand(Command):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("context_settings", {"help_option_names": ("--help", "--my-fancy-help")})
        super().__init__(*args, **kwargs)


class CustomGroup(Group):

    command_class = CustomCommand


@group(cls=CustomGroup)
def my_cli():
    pass


@my_cli.command()
def subcommand():
    pass


if __name__ == "__main__":
    my_cli()
```

When I call the bare CLI at the group level, the `subcommand` is properly registered and appears in the help screen:
```shell-session
$ python ./cloup_test.py 
Usage: cloup_test.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  subcommand
```

Now when I call the `--help` on the `subcommand` I cannot see any reference to my `--my-fancy-help` custom help option name:

```shell-session
$ python ./cloup_test.py subcommand --help
Usage: cloup_test.py subcommand [OPTIONS]

Options:
  --help  Show this message and exit.
```

#### Expected behavior

Instead of the output above, I expect to get the following results:

```shell-session
$ python ./cloup_test.py subcommand --help
Usage: cloup_test.py subcommand [OPTIONS]

Options:
  --help, --my-fancy-help  Show this message and exit.
```

Notice how `--my-fancy-help` is featured in the help screen, because I expect `@my_cli.command()` to return a decorator of `CustomCommand`, as per the `command_class` property defined on `CustomGroup`.

#### Click behavior

The same minimal CLI, sourced with Click's primitives, is working as expected.

In the example above, if you replace:
```python
from cloup import Command, Group, group
```

With:
```python
from click import Command, Group, group
```

You get the expected output:
```shell-session
$ python ./cloup_test.py subcommand --help
Usage: cloup_test.py subcommand [OPTIONS]

Options:
  --my-fancy-help, --help  Show this message and exit.
```

#### Notes

- This might be related to https://github.com/pallets/click/pull/2417 , which has been fixed in the recent Click 8.1.4

- This example is [inspired by Click's unittest](https://github.com/pallets/click/blob/d9af5cfa009c927a96d10ed38a3e37979876a12e/tests/test_command_decorators.py#L14-L31)
