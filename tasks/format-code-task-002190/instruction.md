When using the ~~--debug option~~ `DEBUG` environment variable in the sample command, the debug value is not correctly set (`flag_value`). It is expected to be either `logging.DEBUG` or `None`, but it seems to be getting the integer value directly from the environment variable.

Sample:

```python
import logging
import os
import sys

import click


# Works as expected
# sys.argv = ['', '--debug']

# Does not work as expected
# os.environ['DEBUG'] = '1'

@click.command()
@click.option('--debug', is_flag=True, flag_value=logging.DEBUG, envvar='DEBUG')
def sample(debug):
    click.echo(f"DEBUG: {debug}")
    assert debug in [logging.DEBUG, None], f"Invalid debug value: {debug} - expected >{logging.DEBUG}< or None"


if __name__ == '__main__':
    sample()

```

There is no different in using `os.environ` or  `DEBUG=1 python cli.py`.

`DEBUG=8 python cli.py` prints out: `8`

Environment:

- Python version: 3.12.4
- Click version: 8.1.7
